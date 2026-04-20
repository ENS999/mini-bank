class UserWorker:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_user(self, user_name, password):
        self.cursor.execute(
            "INSERT INTO user (user_name, password) VALUES (?, ?)",
            (user_name, password)
        )
        return self.cursor.lastrowid

    def get_user(self, user_id):
        self.cursor.execute(
            "SELECT * FROM user WHERE id = ?",
            (user_id,)
        )
        return self.cursor.fetchone()
    
    def get_user_by_name(self, user_name):
        self.cursor.execute(
            "SELECT * FROM user WHERE user_name = ?",
            (user_name,)
        )
        return self.cursor.fetchone()