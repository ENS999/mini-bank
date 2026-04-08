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