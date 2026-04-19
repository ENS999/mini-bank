## Mini Bank API

這是一個模擬銀行的操作系統，在這個系統裡實現了透過FastAPI進行交互功能。
專案裡的功能如:創建帳戶，擁有ACID的存取款，以及提供交易紀錄和查詢的功能。

This project is a banking system simulation that utilizes FastAPI for seamless interaction.
It features robust functionalities such as account management, ACID-guaranteed deposits and withdrawals, and a comprehensive system for querying transaction records.

## How to run

1. Clone the repo

```bash
git clone https://github.com/ENS999/mini-bank.git
```

2. Install dependencies

```bash
pip install fastapi uvicorn
```

3. Run the server

```bash
cd py/mini_bank
python app.py
```

4. Open browser

```
http://127.0.0.1:8000/docs
```

--

## API Endpoints

- POST /register — 註冊帳戶
- POST /deposit — 存款
- POST /withdrawal — 取款
- GET /balance/{account_id} — 查詢餘額
- GET /transactions/{account_id} — 查詢交易紀錄
