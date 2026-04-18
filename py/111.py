import sqlite3

def get_current_balance():
    with sqlite3.connect("bank.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT balance
                       FROM transactions
                       ORDER BY id DESC
                       LIMIT 1
                       """)
        balance = cursor.fetchone()
        if not balance:
            return 0.0
        else:
            return balance
print(get_current_balance())