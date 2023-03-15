from model.entity import Entity


class User(Entity):
    def __init__(self, user_id, username, password, admin=False):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.admin = admin

    def get_id(self):
        return self.user_id

    def set_id(self, entity_id):
        self.user_id = entity_id
