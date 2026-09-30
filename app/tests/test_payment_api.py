import pytest
import json
import sys
import os

# Add parent directory to sys.path so app can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["author"] == "he99codes"
    assert "PayShield" in data["service"]

def test_health_check(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "HEALTHY"
    assert data["dependencies"]["fraud_engine"] == "ACTIVE"
    assert data["dependencies"]["pci_dss_compliance"] == "VERIFIED"

def test_successful_transaction(client):
    payload = {
        "amount": 250.75,
        "currency": "USD",
        "sender_account": "ACC-78901",
        "recipient_account": "ACC-12345"
    }
    response = client.post('/api/v1/transactions', 
                           data=json.dumps(payload), 
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["success"] is True
    assert data["transaction"]["status"] == "AUTHORIZED"
    assert data["transaction"]["amount"] == 250.75
    assert data["transaction"]["authorization_code"].startswith("AUTH-")

def test_fraud_flagged_transaction(client):
    payload = {
        "amount": 75000.00,
        "currency": "USD",
        "sender_account": "ACC-78901",
        "recipient_account": "ACC-12345"
    }
    response = client.post('/api/v1/transactions', 
                           data=json.dumps(payload), 
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["transaction"]["status"] == "FLAGGED_FOR_REVIEW"
    assert data["transaction"]["risk_score"] > 80

def test_invalid_payload(client):
    payload = {"amount": -10}
    response = client.post('/api/v1/transactions', 
                           data=json.dumps(payload), 
                           content_type='application/json')
    assert response.status_code == 400

def test_prometheus_metrics_export(client):
    response = client.get('/api/v1/metrics')
    assert response.status_code == 200
    assert b"payshield_requests_total" in response.data
