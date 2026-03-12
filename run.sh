#!/usr/bin/env bash
set -euo pipefail

if ! command -v ollama >/dev/null 2>&1; then
  echo "Error: ollama is not installed or not in PATH"
  exit 1
fi

echo "Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

cleanup() {
  kill "$OLLAMA_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "Starting FastAPI server..."
uvicorn backend.main:app --reload
