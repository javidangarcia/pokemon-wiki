from flask_login import UserMixin
import uuid

class User(UserMixin):
    def __init__(self, username, password):
        self.id = uuid.uuid4()
        self.username = username
        self.password = password