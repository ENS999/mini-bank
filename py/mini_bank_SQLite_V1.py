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

class UserWorker:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_user(self, user_name):
        self.cursor.execute(
            "INSERT INTO user (user_name) VALUES (?)",
            (user_name,)
        )
        return self.cursor.lastrowid

    def get_user(self, user_id):
        self.cursor.execute(
            "SELECT * FROM user WHERE id = ?",
            (user_id,)
        )
        return self.cursor.fetchone()

class AccountWorker:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_user_account(self, user_id, account_type):
        self.cursor.execute(
            "INSERT INTO user_account (user_id, account_type) VALUES (?, ?)",
            (user_id, account_type)
        )

    def handle_deposit(self, account_id, amount):
        self.cursor.execute(
            "UPDATE user_account SET balance = balance + ? WHERE id = ?",
            (amount, account_id)
        )

    def handle_withdraw(self, account_id, amount):
        self.cursor.execute(
            "UPDATE user_account SET balance = balance - ? WHERE id = ?",
            (amount, account_id)
        )

    def get_balance(self, account_id):
        self.cursor.execute(
            "SELECT balance FROM user_account WHERE id = ?",
            (account_id,)
        )
        result = self.cursor.fetchone()
        if result is None:
            return 0
        return result[0]

    def get_account_id_by_user(self, user_id):
        self.cursor.execute(
            "SELECT id FROM user_account WHERE user_id = ?",
            (user_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

class TransactionWorker:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_transactions(self, account_id, trans_type, amount, target):
        self.cursor.execute(
            "INSERT INTO transactions (account_id, type, amount, target) VALUES (?, ?, ?, ?)",
            (account_id, trans_type, amount, target)
        )
    
    def get_transactions(self, account_id): 
        self.cursor.execute(
            "SELECT * FROM transactions WHERE account_id = ?",
            (account_id,)
        )

        return self.cursor.fetchall()

manager = BankManager("bank.db")
manager.create_table()
cursor = manager.get_cursor()

user_worker = UserWorker(cursor)
account_worker = AccountWorker(cursor)
transaction_worker = TransactionWorker(cursor)

def handle_deposit(manager, account_worker, transaction_worker, account_id):
    amount = get_valid_amount("Enter your amount: ")
    if amount is None:
        return None
    try:
        account_worker.handle_deposit(account_id, amount)
        transaction_worker.create_transactions(account_id, "Deposit", amount, "Self")
        manager.connection.commit()

        balance = account_worker.get_balance(account_id)
        print(f"Deposit successful. Your balance: {balance:.2f}")
    except Exception:
        manager.connection.rollback()
        print("Transaction failed.")


def handle_withdrawal(manager, account_worker, transaction_worker, account_id):
    balance = account_worker.get_balance(account_id)
    if balance <= 0:
        print(f"Your balance: {balance:.2f}")
        return
    while True:
        amount = get_valid_amount("Enter your amount: ")
        if amount is None:
            return
        if amount > balance:
            print(f"Your balance: {balance:.2f}")
            continue

        try:
            account_worker.handle_withdraw(account_id, amount)
            transaction_worker.create_transactions(account_id, "Withdraw", amount, "Self")
            manager.connection.commit()

            balance = account_worker.get_balance(account_id)
            print(f"Withdrawal successful. Your balance: {balance:.2f}")
            return
        except Exception:
            manager.connection.rollback()
            print("Transaction failed.")
            return

def get_valid_amount(prompt):
    while True:
      amount_raw = input(prompt).strip()
      if amount_raw.lower() == "q":
          return None
      try:
          amount = float(amount_raw)
      except ValueError:
          print("Please enter a number, or press 'Q' to go back.")
          continue
      if amount <= 0:
          print("Amount must be greater than 0.")
          continue
      return amount


def register(manager, user_worker, account_worker):
    name = input("Enter your name: ").strip()
    try:
        user_id = user_worker.create_user(name)
        account_worker.create_user_account(user_id, "savings")
        manager.connection.commit()
        print(f"Register successful. Your user ID is {user_id}.")
        return
    except Exception:
        manager.connection.rollback()
        print("Registration failed.")
        return

def login(user_worker):
    while True:
        user_id = input("Enter your ID: ").strip()
        try:
            user_id = int(user_id)
            if user_id <= 0:
                print("ID must be greater than 0.")
                continue
        except ValueError:
            print("Please enter a number.")
            continue
        user = user_worker.get_user(user_id)
        if user is None:
            print("User not found.")
            continue
        return user_id

def show_transactions(transaction_worker, account_id):
    result = transaction_worker.get_transactions(account_id)
    if not result:
        print("No transactions found.")
        return
    for data in result:
        print(f"Account ID: {data[1]}. Type: {data[2]}, Amount: {data[3]:.2f}, Target: {data[4]} {data[5]}")

def get_summary(account_worker, transaction_worker, account_id):
    txs = transaction_worker.get_transactions(account_id)
    if not txs:
        print("No transactions found.")
        return

    deposit_count = 0
    deposit_total = 0.0
    withdrawal_count = 0
    withdrawal_total = 0.0

    for tx in txs:
        if tx[2] == "Deposit":
            deposit_count += 1
            deposit_total += tx[3]
        elif tx[2] == "Withdraw":
            withdrawal_count += 1
            withdrawal_total += tx[3]
    get_balance = account_worker.get_balance(account_id)
    print("=")
    print(f"Deposit Count: 【{deposit_count}】")
    print(f"Deposit Total: 【{deposit_total:.2f}】")
    print(f"Withdrawal Count: 【{withdrawal_count}】")
    print(f"Withdrawal Total: 【{withdrawal_total:.2f}】")
    print(f"Current Balance: 【{get_balance:.2f}】")
    print("=")

def get_choice():
    print("===Welcome to Mini Bank===")
    print("Enter '1' to deposit")
    print("Enter '2' to withdraw")
    print("Enter '3' to check balance")
    print("Enter '4' to view transaction history")
    print("Enter '5' to view summary")
    print("Enter '0' to exit")
    choice = input("Enter your choice here: ").strip()
    return choice

try:
    print("1：Login")
    print("2：Register")
    action = input("Enter your choice: ").strip()
    if action == "2":
        register(manager, user_worker, account_worker)  
    user_id = login(user_worker)
    account_id = account_worker.get_account_id_by_user(user_id)

    while True:
        choice = get_choice()
        if choice == "1":
            handle_deposit(manager, account_worker, transaction_worker, account_id)

        elif choice == "2":
            handle_withdrawal(manager, account_worker, transaction_worker, account_id)

        elif choice == "3":
            balance = account_worker.get_balance(account_id)
            print(f"Your current balance: {balance:.2f}")

        elif choice == "4":
            show_transactions(transaction_worker, account_id)

        elif choice == "5":
            get_summary(account_worker, transaction_worker, account_id)

        elif choice == "0":
            print("Thank you for using Mini Bank.")
            break

        else:
            print("Please enter a number 1/2/3/4/5/0.")
            continue
finally:
    manager.close()