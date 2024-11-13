class User:
    def __init__(self, user_id, username, join_date):
        self.user_id = user_id
        self.username = username
        self.join_date = join_date

    def get_info(self):
        return f"User: {self.username}, Joined: {self.join_date}"
