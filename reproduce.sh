#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "    EpiGraph: End-to-End One-Click Reproduction Suite     "
echo "=========================================================="

PYTHON_BIN="/Users/tejap/anaconda3/bin/python3"
if ! command -v "$PYTHON_BIN" &> /dev/null; then
    PYTHON_BIN="python3"
fi

echo "[1/4] Verifying Graph Scaling Stress Test..."
$PYTHON_BIN run_scaling_benchmark.py

echo "[2/4] Verifying Knowledge Updates & Contradiction Resolution..."
$PYTHON_BIN run_knowledge_update_eval.py

echo "[3/4] Running Automated Hallucination Verification Suite..."
$PYTHON_BIN verify_hallucinations.py

echo "=========================================================="
echo ">>> All reproduction and verification checks passed! <<<"
echo "=========================================================="
