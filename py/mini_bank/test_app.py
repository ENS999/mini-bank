from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_register():
    response = client.post("/register", json={
        "name": "test",
        "account_type": "savings"
    })
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "account_id" in data

def test_deposit():
    reg = client.post("/register", json={
        "name": "Test2",
        "account_type": "savings"
    })
    account_id = reg.json()['account_id']

    response = client.post("/deposit", json={
        "account_id": account_id,
        "amount": 1000
    })
    assert response.status_code == 200

    balance = client.get(f"/balance/{account_id}")
    assert balance.json()['balance'] == 1000

def test_invaild_account():
    response = client.post("/deposit", json={
        "account_id": 999,
        "amount": 1000
    })
    assert response.status_code == 404

    response_two = client.post("/withdrawal", json={
        "account_id": 999,
        "amount": 1000
    })
    assert response_two.status_code == 404

def test_withdrawal():
    reg = client.post("/register", json={
        "name": "Test3",
        "account_type": "savings"
    })
    account_id = reg.json()['account_id']

    response = client.post("/deposit", json={
        "account_id": account_id,
        "amount": 1000
    })
    response = client.post("/withdrawal", json={
        "account_id": account_id,
        "amount": 500
    })
    assert response.status_code == 200

    balance = client.get(f"/balance/{account_id}")
    assert balance.json()['balance'] == 500

def test_withdrawal_insufficient():
    reg = client.post("/register", json={
        "name": "Test4",
        "account_type": "savings"
    })
    account_id = reg.json()['account_id']

    response = client.post("/withdrawal", json={
        "account_id": account_id,
        "amount": 10000
    })
    assert response.status_code == 400

def test_negative_amount():
    response = client.post("/deposit", json={
        "account_id": 1,
        "amount": -100
    })
    assert response.status_code == 422

    response_two = client.post("/withdrawal", json={
        "account_id": 1,
        "amount": -100
    })
    assert response_two.status_code == 422