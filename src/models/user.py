from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from src.ext import db
from src.models.base import BaseModel

class User(BaseModel, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    _password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return self.username

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    password = db.synonym('_password', descriptor=property(_get_password, _set_password))