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