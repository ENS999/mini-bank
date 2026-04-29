# Mini Bank API

這是一個模擬銀行的操作系統，透過 FastAPI 實現 RESTful API。功能包含：帳戶創建、JWT 認證與授權、ACID 保證的存取款、以及交易紀錄查詢。

This project is a banking system simulation built with FastAPI. It features account management, JWT authentication & authorization, ACID-guaranteed deposits and withdrawals, and transaction record queries.

**Live Demo:** https://mini-bank-tp1k.onrender.com/docs

---

## Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI
- **Database:** SQLite
- **Authentication:** JWT (python-jose + passlib bcrypt)
- **Validation:** Pydantic
- **Testing:** pytest (11 tests)
- **Containerization:** Docker
- **Deployment:** Render

---

## Project Structure

```
mini_bank/
├── app.py              # API routes, JWT auth
├── main.py             # Entry point
├── models/
│   └── manager.py      # BankManager (business logic)
├── services/           # Worker layer
├── utils/              # Utility functions
├── test_app.py         # pytest test cases
├── Dockerfile
├── requirements.txt
├── .env.example
└── .dockerignore
```

---

## API Endpoints

| Method | Endpoint                     | Description  | Auth |
| ------ | ---------------------------- | ------------ | ---- |
| POST   | `/register`                  | 註冊帳戶     | No   |
| POST   | `/login`                     | 登入取得 JWT | No   |
| POST   | `/deposit`                   | 存款         | Yes  |
| POST   | `/withdrawal`                | 取款         | Yes  |
| GET    | `/balance/{account_id}`      | 查詢餘額     | Yes  |
| GET    | `/transactions/{account_id}` | 查詢交易紀錄 | Yes  |

---

## How to Run

### Local

Clone the repo and enter the project directory:

```
git clone https://github.com/ENS999/mini-bank.git
cd mini-bank/py/mini_bank
```

Install dependencies:

```
pip install -r requirements.txt
```

Set up environment variables:

```
cp .env.example .env
```

Edit `.env` and set your own `SECRET_KEY`.

Run the server:

```
uvicorn app:app --reload
```

Open browser: http://127.0.0.1:8000/docs

### Docker

```
docker build -t mini-bank .
docker run --env-file .env -p 8000:8000 mini-bank
```

Open browser: http://localhost:8000/docs

---

## Run Tests

```
pytest test_app.py -v
```
