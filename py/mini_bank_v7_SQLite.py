import sqlite3

def init_db():
    conn = sqlite3.connect("bank.db")
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS transactions (
                           id INTEGER PRIMARY KEY,
                           type TEXT,
                           amount REAL,
                           balance REAL,
                           note TEXT)
                           """)
    finally:
        conn.close()

def get_current_balance():
    conn = sqlite3.connect("bank.db")
    try:
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT balance
                        FROM transactions
                        ORDER BY id DESC
                        LIMIT 1
                        """)
        row = cursor.fetchone()
        if row is None:
            return 0.0
        else:
            return row[0]
    finally:
        conn.close()

def add_transaction(tx_type, amount, balance, note):
    conn = sqlite3.connect("bank.db")
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO transactions (type, amount, balance, note)
                           VALUES (?, ?, ?, ?)
                           """, (tx_type, amount, balance, note))
    finally:
        conn.close()

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

def get_note():
    while True:
        note = input("Enter note (Max len 10) or Leave it blank: ").strip()
        if len(note) > 10:
            print("Note is too long.")
            continue
        elif note == "":
            return "No note"
        return note

def handle_deposit():
    amount = get_valid_amount("Please enter your deposit amount, or press 'Q' to go back: ")
    if amount is None:
        return
    note = get_note()
    balance = get_current_balance()
    balance += amount
    add_transaction("deposit", amount, balance, note)
    print(f"Deposit successful. Your balance: {balance:.2f}")

def handle_withdrawal():
    while True:
        balance = get_current_balance()
        if balance <= 0:
            print(f"Your balance: {balance:.2f}")
            return
        amount = get_valid_amount("Please enter your withdrawal amount, or press 'Q' to go back: ")
        if amount is None:
            return
        if amount > balance:
            print(f"Your balance: {balance:.2f}")
            continue
        note = get_note()
        balance -= amount
        add_transaction("withdrawal", amount, balance, note)
        print(f"Withdrawal successful. Your balance: {balance:.2f}")
        return

def show_transactions():
    conn = sqlite3.connect("bank.db")
    try:
        with conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions ORDER BY id ASC")
            rows = cursor.fetchall()
            if not rows:
                print("No transactions found.")
                return

            for i, row in enumerate(rows, start=1):
                note = row['note'] or "No note"
                print(f"{i}. Type: {row['type'].title()}, Amount: {row['amount']:.2f}, Balance: {row['balance']:.2f}, Note: {note}")
    finally:
        conn.close()

def show_summary():
    conn = sqlite3.connect("bank.db")
    try:
        with conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions ORDER BY id ASC")
            rows = cursor.fetchall()
            if not rows:
                print("No transactions found.")
                return

            deposit_count = 0
            deposit_total = 0.0
            withdrawal_count = 0
            withdrawal_total = 0.0

            for row in rows:
                if row["type"] == "deposit":
                    deposit_count += 1
                    deposit_total += row["amount"]
                elif row["type"] == "withdrawal":
                    withdrawal_count += 1
                    withdrawal_total += row["amount"]
            current_balance = get_current_balance()
            print("=")
            print(f"Deposit Count: 【{deposit_count}】")
            print(f"Deposit Total: 【{deposit_total:.2f}】")
            print(f"Withdrawal Count: 【{withdrawal_count}】")
            print(f"Withdrawal Total: 【{withdrawal_total:.2f}】")
            print(f"Current Balance: 【{current_balance:.2f}】")
            print("=")
    finally:
        conn.close()

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
if __name__ == "__main__":
    init_db()

    while True:
        choice = get_choice()
        if choice == "1":
            handle_deposit()

        elif choice == "2":
            handle_withdrawal()

        elif choice == "3":
            balance = get_current_balance()
            print(f"Your current balance: {balance:.2f}")

        elif choice == "4":
            show_transactions()

        elif choice == "5":
            show_summary()

        elif choice == "0":
            print("Thank you for using Mini Bank.")
            break

        else:
            print("Please enter a number 1/2/3/4/5/0.")
            continue