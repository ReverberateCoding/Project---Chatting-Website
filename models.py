from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    hashed_pswd = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'User with username: {self.username} and password: {self.hashed_pswd}'
