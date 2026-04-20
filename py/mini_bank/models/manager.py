import sqlite3
from .user_worker import UserWorker
from .account_worker import AccountWorker
from .transaction_worker import TransactionWorker
from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-secret-key-change-this"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])

class BankManager:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
    
    def get_cursor(self):
        return self.connection.cursor()
    
    def close(self):
        self.connection.close()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
               CREATE TABLE IF NOT EXISTS user (
               id INTEGER PRIMARY KEY,
               user_name TEXT UNIQUE,
               password TEXT
               )
               """)
        cursor.execute("""
               CREATE TABLE IF NOT EXISTS user_account (
               id INTEGER PRIMARY KEY,
               user_id INTEGER,
               account_type TEXT,
               balance REAL DEFAULT 0,
               FOREIGN KEY (user_id) REFERENCES user(id)
               )
               """)
        cursor.execute("""
               CREATE TABLE IF NOT EXISTS transactions (
               id INTEGER PRIMARY KEY,
               account_id INTEGER,
               type TEXT,
               amount REAL,
               target TEXT,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (account_id) REFERENCES user_account(id)
               )
               """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_account_user_id ON user_account(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id)")
        self.connection.commit()
        cursor.close()

    def register(self, name, password, account_type):
        cursor = self.connection.cursor()
        try:
            user_worker = UserWorker(cursor)
            account_worker = AccountWorker(cursor)
            hashed_password = pwd_context.hash(password)
            user_id = user_worker.create_user(name, hashed_password)
            account_worker.create_user_account(user_id, account_type)
            account_id = account_worker.get_account_id_by_user(user_id)
            self.connection.commit()
            return {"user_id": user_id, "account_id": account_id}
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def login(self, name, password):
        cursor = self.connection.cursor()
        try:
            user_worker = UserWorker(cursor)
            user = user_worker.get_user_by_name(name)
            if user is None:
                raise HTTPException(status_code=401, detail="invalid credentials")
            if not pwd_context.verify(password, user[2]):
                raise HTTPException(status_code=401, detail="invalid credentials")
            token = jwt.encode(
                {"user_id": user[0], "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
                SECRET_KEY,
                algorithm=ALGORITHM
            )
            return token
        except HTTPException:
            raise
        finally:
            cursor.close()

    def deposit(self, account_id, amount):
        cursor = self.connection.cursor()
        try:
            account_worker = AccountWorker(cursor)
            transaction_worker = TransactionWorker(cursor)
            balance = account_worker.get_balance(account_id)
            if balance is None:
                raise HTTPException(status_code=404, detail="account not found")
            account_worker.handle_deposit(account_id, amount)
            transaction_worker.create_transactions(account_id, "deposit", amount, None)
            self.connection.commit()
            return
        except HTTPException:
            raise
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def withdrawal(self, account_id, amount):
        cursor = self.connection.cursor()
        try:
            account_worker = AccountWorker(cursor)
            transaction_worker = TransactionWorker(cursor)
            balance = account_worker.get_balance(account_id)
            if balance is None:
                raise HTTPException(status_code=404, detail="account not found")
            if balance < amount:
                raise HTTPException(status_code=400, detail="insufficient balance")
            account_worker.handle_withdraw(account_id, amount)
            transaction_worker.create_transactions(account_id, "withdraw", amount, None)
            self.connection.commit()
            return
        except HTTPException:
            raise
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def get_balance(self, account_id):
        cursor = self.connection.cursor()
        try:
            account_worker = AccountWorker(cursor)
            balance = account_worker.get_balance(account_id)
            if balance is None:
                raise HTTPException(status_code=404, detail="account not found")
            return balance
        finally:
            cursor.close()

    def get_transactions(self, account_id):
        cursor = self.connection.cursor()
        try:
            account_worker = AccountWorker(cursor)
            transaction_worker = TransactionWorker(cursor)
            balance = account_worker.get_balance(account_id)
            if balance is None:
                raise HTTPException(status_code=404, detail="account not found")
            rows = transaction_worker.get_transactions(account_id)
            return [
                {
                    "account_id": r[1],
                    "type": r[2],
                    "amount": r[3],
                    "target": r[4],
                    "timestamp": r[5]
                }
                for r in rows
            ]
        finally:
            cursor.close()