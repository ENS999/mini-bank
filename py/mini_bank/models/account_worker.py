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
            return
        return result[0]

    def get_account_id_by_user(self, user_id):
        self.cursor.execute(
            "SELECT id FROM user_account WHERE user_id = ?",
            (user_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def verify_owner(self, account_id, user_id):
        self.cursor.execute(
            "SELECT user_id FROM user_account WHERE id = ?",
            (account_id,)
        )
        result = self.cursor.fetchone()
        if result is None:
            return None
        return result[0] == user_id