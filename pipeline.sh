#!/usr/bin/env bash
set -e

echo "[Stage 1/4] Linting code..."
python3 -m py_compile app.py

echo "[Stage 2/4] Executing automated tests..."
pytest test_app.py -q

echo "[Stage 3/4] Building Docker artifact..."
docker build -t my-app:latest .

echo "[Stage 4/4] Deploying container locally..."
docker stop my-app-prod || true
docker rm my-app-prod || true
docker run -d --name my-app-prod -p 5000:5000 my-app:latest

echo "Pipeline executed successfully! Health check:"
curl -s http://localhost:5000
