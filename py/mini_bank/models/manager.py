import sqlite3

class BankManager:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
    
    def get_cursor(self):
        return self.connection.cursor()
    
    def close(self):
        self.connection.close()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
               CREATE TABLE IF NOT EXISTS user (
               id INTEGER PRIMARY KEY,
               user_name TEXT
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