import sqlite3

conn = sqlite3.connect("test_bank")
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE user (
               id INTEGER PRIMARY KEY,
               user_name TEXT
               )
               """)

cursor.execute("""
               CREATE TABLE IF NOT EXISTS user_account (
               id INTEGER PRIMARY KEY,
               user_id INTEGER,
               account_type TEXT,
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

cursor.execute("CREATE INDEX idx_user_account_user_id ON user_account(user_id)")
cursor.execute("CREATE INDEX idx_treansactions_account_id ON transactions(account_id)")