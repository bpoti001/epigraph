#!/usr/bin/env bash
set -e

REPO_NAME="epigraph"
GITHUB_USER="bpoti001"
PAT="${1:-${GITHUB_PAT}}"

if [ -z "$PAT" ]; then
    echo "Usage: ./push_to_github.sh <GITHUB_PAT>"
    echo "Or set export GITHUB_PAT=..."
    exit 1
fi

echo "=========================================================="
echo "    Pushing EpiGraph to GitHub: ${GITHUB_USER}/${REPO_NAME}"
echo "=========================================================="

# Check if remote repository exists
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token ${PAT}" "https://api.github.com/repos/${GITHUB_USER}/${REPO_NAME}")

if [ "$HTTP_CODE" -eq 404 ]; then
    echo "Notice: Repository '${GITHUB_USER}/${REPO_NAME}' does not exist on GitHub yet."
    echo "GitHub fine-grained PATs require the repository to be created on GitHub web first."
    echo ""
    echo "👉 Please create the empty repository in 1 click here:"
    echo "   https://github.com/new?name=${REPO_NAME}&description=EpiGraph%3A+Dynamic+Usage-Weighted+Topology+and+Synaptic+Consolidation+for+Multi-Hop+Agentic+Memory"
    echo ""
    echo "(Leave 'Initialize with README' UNCHECKED, then run this script again)"
    exit 1
fi

echo "Repository found on GitHub! Setting up origin and pushing..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://${GITHUB_USER}:${PAT}@github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "Pushing 'main' branch..."
git -c credential.helper= push -u origin main

echo ""
echo "Cleaning up credentials from local git config..."
git remote set-url origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

echo "=========================================================="
echo ">>> Successfully pushed to https://github.com/${GITHUB_USER}/${REPO_NAME} <<<"
echo "=========================================================="
