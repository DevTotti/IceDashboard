"""Data models."""
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from ..app import db
from flask_login import UserMixin

# The User class is a data model for user accounts
class User(UserMixin, db.Model):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    transaction = db.relationship('Transaction', backref='done_by', cascade='all, delete')
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)

    def __init__(self, **kwargs):
        """
        The function takes in a dictionary of keyword arguments and assigns the values to the class
        attributes
        """
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha512')

    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        return True
        
    @property
    def is_active(self):
        return True

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }




class Role(db.Model):

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    role_link = db.relationship('UserRole', cascade='all, delete-orphan', uselist=False)

    def __str__(self):
        return self.name


class UserRole(db.Model):

    __tablename__ = "user_roles"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    user_role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)
    last_modified = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)