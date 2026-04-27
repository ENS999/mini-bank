from fastapi.testclient import TestClient
from app import app
from models import BankManager

test_manager = BankManager(":memory:")
test_manager.create_table()

import app as app_module
app_module.manager = test_manager

client = TestClient(app)

def register_and_login(name, password):
    reg = client.post("/register", json={
        "name": name,
        "password": password,
        "account_type": "savings"
    })
    response = client.post("/login", json={
        "name": name,
        "password": password
    })
    headers = {"Authorization": f"Bearer {response.json()['token']}"}
    account_id = reg.json()['account_id']
    return headers, account_id

def test_register():
    response = client.post("/register", json={
        "name": "test_register",
        "password": "123456",
        "account_type": "savings"
    })
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "account_id" in data

def test_login():
    client.post("/register", json={
        "name": "Test_login",
        "password": "123456",
        "account_type": "savings"
    })

    response = client.post("/login", json={
        "name": "Test_login",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_password_error():
    client.post("/register", json={
        "name": "Test_test_login_password_error",
        "password": "123456",
        "account_type": "savings"
    })

    response = client.post("/login", json={
        "name": "Test_test_login_password_error",
        "password": "1234567"
    })
    assert response.status_code == 401

def test_login_account_error():
    client.post("/register", json={
        "name": "Test_login_account_error",
        "password": "123456",
        "account_type": "savings"
    })

    response = client.post("/login", json={
        "name": "Test_account_error",
        "password": "123456"
    })
    assert response.status_code == 401

def test_not_token():
    headers, account_id = register_and_login("Test_not_token", "123456")
    dp_response = client.post("/deposit", json={
        "account_id": account_id,
        "amount": 1000
    })
    assert dp_response.status_code == 401

    wd_response = client.post("/withdrawal", json={
        "account_id": account_id,
        "amount": 1000
    })
    assert wd_response.status_code == 401

def test_deposit():
    headers, account_id = register_and_login("Test_deposit", "123456")

    response = client.post("/deposit", json={
        "account_id": account_id,
        "amount": 1000
    }, headers=headers)
    assert response.status_code == 200

    balance = client.get(f"/balance/{account_id}", headers=headers)
    assert balance.json()['balance'] == 1000

def test_invalid_account():
    headers, account_id = register_and_login("Test_invalid_account", "123456")

    response = client.post("/deposit", json={
        "account_id": 999,
        "amount": 1000
    }, headers=headers)
    assert response.status_code == 404

    response_two = client.post("/withdrawal", json={
        "account_id": 999,
        "amount": 1000
    }, headers=headers)
    assert response_two.status_code == 404

def test_withdrawal():
    headers, account_id = register_and_login("Test_withdrawal", "123456")

    response = client.post("/deposit", json={
        "account_id": account_id,
        "amount": 1000
    }, headers=headers)

    response = client.post("/withdrawal", json={
        "account_id": account_id,
        "amount": 500
    }, headers=headers)
    assert response.status_code == 200

    balance = client.get(f"/balance/{account_id}", headers=headers)
    assert balance.json()['balance'] == 500

def test_withdrawal_insufficient():
    headers, account_id = register_and_login("Test_withdrawal_insufficient", "123456")

    response = client.post("/withdrawal", json={
        "account_id": account_id,
        "amount": 10000
    }, headers=headers)
    assert response.status_code == 400

def test_negative_amount():
    headers, account_id = register_and_login("Test_negative_amount", "123456")

    response = client.post("/deposit", json={
        "account_id": 1,
        "amount": -100
    }, headers=headers)
    assert response.status_code == 422

    response_two = client.post("/withdrawal", json={
        "account_id": 1,
        "amount": -100
    }, headers=headers)
    assert response_two.status_code == 422

def test_forbidden():
    user_a, account_id_a = register_and_login("User_a", "123456")
    user_b, account_id_b = register_and_login("User_b", "123456")

    client.post("/deposit", json={
        "account_id": account_id_b,
        "amount": 1000
    }, headers=user_b)

    use_user_a_withdrawal = client.post("/withdrawal", json={
        "account_id": account_id_b,
        "amount": 1000
    }, headers=user_a)
    assert use_user_a_withdrawal.status_code == 403