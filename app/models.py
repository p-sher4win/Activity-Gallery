from mongoengine import Document, StringField, ListField, DateTimeField
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Activity Model
class Activity(Document):
    title = StringField(required=True)
    img_urls = ListField(StringField(), required=True)
    date_added = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'activities'}

    def __repr__(self):
        return f"Activity {self.title}: {self.date_added}"
    
# User Model
class User(Document, UserMixin):
    name = StringField(required=True, max_length=50)
    username = StringField(required=True, max_length=50)
    date_created = DateTimeField(default=datetime.utcnow)

    # Password Hashing
    password_hash = StringField(required=True)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")
    
    @password.setter
    def password(self, pswd):
        self.password_hash = generate_password_hash(pswd)

    def verify_password(self, pswd):
        return check_password_hash(self.password_hash, pswd)
    
    def get_id(self):
        return str(self.id)

    meta = {'collection': 'users'}

    def __repr__(self):
        return f"User {self.username}"