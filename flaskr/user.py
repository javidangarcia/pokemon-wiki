from flask_login import UserMixin
'''This module contains the user class used for creating users in the application.'''


class User(UserMixin):

    def __init__(self, username, password):
        '''User constructor.

           Args:
            id: User id
            username: User's selected name
            password: User's selected password
        '''
        self.id = username
        self.username = username
        self.password = password
