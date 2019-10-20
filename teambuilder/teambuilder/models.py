from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(40),
                    nullable=False,
                    unique=True)