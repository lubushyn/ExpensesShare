__author__ = 'aliubushyn'
from flask_login import UserMixin

class User(UserMixin):
    """User Session management Class
    """
    def __init__(self, email=None, id=None, name=None, accesstoken="", active=True):
        self.email = email
        self.id = id
        self.active = active
        self.name = name
        self.accesstoken = accesstoken

    def is_active(self):
        return self.active

    def myemail(self):
        return self.email

    def get_userid(self):
        return self.id

    def get_name(self):
        return  self.name