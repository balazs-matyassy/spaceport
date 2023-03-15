class User:
    def __init__(self, user_id, username, password, admin=False):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.admin = admin
