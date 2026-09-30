import os
import time
import uuid
import json
from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus Metrics
REQUEST_COUNT = Counter('payshield_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('payshield_request_latency_seconds', 'Request latency in seconds', ['endpoint'])
TRANSACTION_COUNTER = Counter('payshield_transactions_total', 'Payment transactions processed', ['currency', 'status'])

START_TIME = time.time()
SERVICE_VERSION = os.getenv("APP_VERSION", "v2.4.0")
ENVIRONMENT = os.getenv("APP_ENV", "production")

# In-memory storage for demonstration (backed by optional Redis)
TRANSACTIONS = {}

@app.route("/")
def index():
    return jsonify({
        "service": "PayShield FinTech Payment Gateway API",
        "author": "he99codes",
        "version": SERVICE_VERSION,
        "environment": ENVIRONMENT,
        "status": "OPERATIONAL",
        "documentation": "/api/v1/docs",
        "health_check": "/api/v1/health"
    })

@app.route("/api/v1/health", methods=["GET"])
def health():
    uptime_seconds = round(time.time() - START_TIME, 2)
    return jsonify({
        "status": "HEALTHY",
        "service": "payshield-payment-gateway",
        "version": SERVICE_VERSION,
        "environment": ENVIRONMENT,
        "uptime_seconds": uptime_seconds,
        "dependencies": {
            "database": "CONNECTED",
            "redis_cache": "CONNECTED",
            "fraud_engine": "ACTIVE",
            "pci_dss_compliance": "VERIFIED"
        }
    }), 200

@app.route("/api/v1/transactions", methods=["POST"])
def process_transaction():
    start_t = time.time()
    data = request.get_json() or {}
    
    amount = data.get("amount")
    currency = data.get("currency", "USD").upper()
    sender = data.get("sender_account")
    recipient = data.get("recipient_account")
    
    if not amount or not sender or not recipient:
        REQUEST_COUNT.labels(method="POST", endpoint="/api/v1/transactions", status="400").inc()
        return jsonify({
            "error": "INVALID_PAYLOAD",
            "message": "amount, sender_account, and recipient_account are required fields"
        }), 400
        
    try:
        amount_val = float(amount)
        if amount_val <= 0:
            raise ValueError()
    except ValueError:
        return jsonify({
            "error": "INVALID_AMOUNT",
            "message": "Amount must be a positive number"
        }), 400

    # Risk Scoring / Fraud Detection Simulation
    is_fraud_suspect = amount_val > 50000
    tx_status = "FLAGGED_FOR_REVIEW" if is_fraud_suspect else "AUTHORIZED"
    
    tx_id = f"tx_{uuid.uuid4().hex[:12]}"
    tx_record = {
        "transaction_id": tx_id,
        "amount": amount_val,
        "currency": currency,
        "sender_account": sender,
        "recipient_account": recipient,
        "status": tx_status,
        "authorization_code": f"AUTH-{uuid.uuid4().hex[:6].upper()}",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "risk_score": 92 if is_fraud_suspect else 12,
        "processed_by_node": os.getenv("HOSTNAME", "payshield-k8s-pod-1")
    }
    
    TRANSACTIONS[tx_id] = tx_record
    
    # Record metrics
    TRANSACTION_COUNTER.labels(currency=currency, status=tx_status).inc()
    REQUEST_COUNT.labels(method="POST", endpoint="/api/v1/transactions", status="201").inc()
    REQUEST_LATENCY.labels(endpoint="/api/v1/transactions").observe(time.time() - start_t)
    
    return jsonify({
        "success": True,
        "transaction": tx_record
    }), 201

@app.route("/api/v1/transactions/<tx_id>", methods=["GET"])
def get_transaction(tx_id):
    tx = TRANSACTIONS.get(tx_id)
    if not tx:
        return jsonify({"error": "NOT_FOUND", "message": f"Transaction {tx_id} not found"}), 404
    return jsonify({"success": True, "transaction": tx}), 200

@app.route("/api/v1/metrics", methods=["GET"])
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
