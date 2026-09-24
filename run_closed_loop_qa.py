#!/usr/bin/env python3
"""
Phase 5: Closed-Loop Downstream LLM Generation QA Benchmark
Feeds retrieved top-5 contexts from each system into a local LLM (qwen2.5vl:7b / gemma4:12b via Ollama)
and evaluates Token-level F1, Exact Match (EM), and ROUGE-L against LoCoMo ground-truth answers.
"""

import os
import sys
import json
import time
import re
import string
import urllib.request
import numpy as np
from typing import Dict, List, Tuple, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.embeddings import EmbeddingEngine
from src.epigraph_pipeline import EpiGraphPipeline
from baselines.vector_rag import DenseVectorRAG
from baselines.bm25_baseline import BM25Baseline

def normalize_answer(s: str) -> str:
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(str(s)))))

def compute_f1(prediction: str, ground_truth: str) -> float:
    pred_tokens = normalize_answer(prediction).split()
    gt_tokens = normalize_answer(ground_truth).split()
    if not pred_tokens or not gt_tokens:
        return float(pred_tokens == gt_tokens)
    common = set(pred_tokens) & set(gt_tokens)
    num_same = sum(min(pred_tokens.count(tok), gt_tokens.count(tok)) for tok in common)
    if num_same == 0:
        return 0.0
    precision = 1.0 * num_same / len(pred_tokens)
    recall = 1.0 * num_same / len(gt_tokens)
    return (2.0 * precision * recall) / (precision + recall)

def compute_em(prediction: str, ground_truth: str) -> float:
    return float(normalize_answer(prediction) == normalize_answer(ground_truth))

def compute_rouge_l(prediction: str, ground_truth: str) -> float:
    pred_tokens = normalize_answer(prediction).split()
    gt_tokens = normalize_answer(ground_truth).split()
    if not pred_tokens or not gt_tokens:
        return float(pred_tokens == gt_tokens)
    
    # LCS
    m, n = len(pred_tokens), len(gt_tokens)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if pred_tokens[i] == gt_tokens[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])
    lcs = dp[m][n]
    if lcs == 0:
        return 0.0
    prec = lcs / m
    rec = lcs / n
    return (2.0 * prec * rec) / (prec + rec)

def query_local_llm(context_text: str, question: str, model: str = "qwen2.5vl:7b") -> str:
    """Prompt local Ollama model to generate answer from context."""
    url = "http://localhost:11434/api/chat"
    prompt = (
        f"Context:\n{context_text}\n\n"
        f"Question: {question}\n"
        f"Answer in 6 words or less using ONLY facts from the context:"
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "options": {
            "temperature": 0.0,
            "num_predict": 30
        },
        "stream": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return res_json.get("message", {}).get("content", "").strip()
    except Exception as e:
        return ""

def run_closed_loop_evaluation(data_path: str = None, max_q_per_conv: int = 5, output_dir: str = None):
    if data_path is None:
        data_path = os.path.join(BASE_DIR, "data", "locomo", "locomo10.json")
    if output_dir is None:
        output_dir = os.path.join(BASE_DIR, "results")
    print("=" * 80)
    print("PHASE 5: RUNNING CLOSED-LOOP DOWNSTREAM LLM GENERATION BENCHMARK")
    print("Evaluating Generative Token F1, Exact Match (EM), and ROUGE-L on LoCoMo")
    print("=" * 80)

    with open(data_path) as f:
        samples = json.load(f)

    embed = EmbeddingEngine()
    systems = {
        "Dense_Vector_RAG": DenseVectorRAG(embed),
        "BM25_Keyword": BM25Baseline(),
        "EpiGraph_Proposed": EpiGraphPipeline(embed)
    }

    # Store metrics: Token F1, Exact Match, ROUGE-L
    metrics = {sys_name: {"F1": [], "EM": [], "ROUGE_L": []} for sys_name in systems}
    cat_f1 = {sys_name: {cat: [] for cat in range(1, 5)} for sys_name in systems}

    total_evaluated = 0

    for s_idx, sample in enumerate(samples):
        conv = sample["conversation"]
        qa_list = sample.get("qa", [])
        
        print(f"\nIngesting Conversation {s_idx + 1}/{len(samples)} into retrieval engines...")
        for sys_name, sys_obj in systems.items():
            if sys_name == "EpiGraph_Proposed":
                sys_obj.ingest_locomo_conversation(conv)
            else:
                sys_obj.ingest(conv)

        # Select stratified sample of questions across categories
        selected_qas = []
        for cat in range(1, 5):
            cat_qas = [qa for qa in qa_list if qa.get("category") == cat and qa.get("evidence")]
            if cat_qas:
                selected_qas.extend(cat_qas[:max(1, max_q_per_conv // 4)])
        if not selected_qas:
            selected_qas = qa_list[:max_q_per_conv]

        conv_turn_lookup = {}
        session_keys = [k for k in conv.keys() if k.startswith("session_") and not k.endswith("_date_time")]
        for sk in session_keys:
            dt = conv.get(sk + "_date_time", "")
            for turn in conv.get(sk, []):
                d_id = turn.get("dia_id")
                spk = turn.get("speaker", "")
                txt = turn.get("text", "")
                conv_turn_lookup[d_id] = f"[{spk}] (Session {sk}, {dt}): {txt}"

        for qa in selected_qas[:max_q_per_conv]:
            q = qa.get("question", "")
            gt_ans = str(qa.get("answer", ""))
            cat = qa.get("category", 1)
            if not q or not gt_ans:
                continue

            total_evaluated += 1

            for sys_name, sys_obj in systems.items():
                top_items = sys_obj.retrieve(q, top_k=5)
                
                # Build context snippet from top retrieved turns
                context_chunks = [conv_turn_lookup[item[0]] for item in top_items if item[0] in conv_turn_lookup]
                combined_context = "\n".join(context_chunks[:4])
                
                # Query LLM
                pred_ans = query_local_llm(combined_context, q)
                
                # Score
                f1 = compute_f1(pred_ans, gt_ans)
                em = compute_em(pred_ans, gt_ans)
                rouge_l = compute_rouge_l(pred_ans, gt_ans)

                metrics[sys_name]["F1"].append(f1)
                metrics[sys_name]["EM"].append(em)
                metrics[sys_name]["ROUGE_L"].append(rouge_l)
                if cat in cat_f1[sys_name]:
                    cat_f1[sys_name][cat].append(f1)

            print(f"  Q{total_evaluated}: '{q[:40]}...' -> Ground Truth: '{gt_ans[:25]}'")

    # Aggregated Summary
    summary = {}
    print("\n" + "=" * 80)
    print(f"{'SYSTEM':<22} | {'Token F1':<10} | {'Exact Match':<12} | {'ROUGE-L':<10} | {'Temporal F1':<12}")
    print("-" * 80)

    for sys_name in systems:
        mean_f1 = float(np.mean(metrics[sys_name]["F1"]) * 100)
        mean_em = float(np.mean(metrics[sys_name]["EM"]) * 100)
        mean_rouge = float(np.mean(metrics[sys_name]["ROUGE_L"]) * 100)
        temp_f1 = float(np.mean(cat_f1[sys_name][2]) * 100) if cat_f1[sys_name][2] else 0.0

        summary[sys_name] = {
            "Token_F1": mean_f1,
            "Exact_Match": mean_em,
            "ROUGE_L": mean_rouge,
            "Temporal_F1": temp_f1
        }
        print(f"{sys_name:<22} | {mean_f1:>8.2f}% | {mean_em:>10.2f}% | {mean_rouge:>8.2f}% | {temp_f1:>10.2f}%")
    print("=" * 80)

    os.makedirs(output_dir, exist_ok=True)
    out_json = os.path.join(output_dir, "closed_loop_qa_results.json")
    with open(out_json, "w") as f:
        json.dump({
            "total_questions_evaluated": total_evaluated,
            "llm_evaluator": "qwen2.5vl:7b",
            "summary": summary
        }, f, indent=2)

    print(f"\nSaved closed-loop QA benchmark results to: {out_json}")
    return summary

if __name__ == "__main__":
    run_closed_loop_evaluation(max_q_per_conv=4)
