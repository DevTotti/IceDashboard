import datetime
from flask_sqlalchemy import SQLAlchemy
from ..app import db

class Transaction(db.Model):

    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reference = db.Column(db.String(16), index=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True)
    description = db.Column(db.String(20), nullable=False)
    narration = db.Column(db.String(20), nullable=True)
    method = db.Column(db.Enum('CARD', 'PAYMENT LINK', 'TRANSFER', name='method'), server_default="CARD", nullable=False)
    direction = db.Column(db.Enum('debit', 'credit', name='direction'), server_default='credit', nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="NGN")

    def __str__(self):
        return self.reference


    def serialize(self):
        return {
            "id": self.id,
            "reference": self.reference,
            "user_id": self.user_id,
            "description": self.description,
            "narration": self.narration,
            "method": self.method,
            "direction": self.direction,
            "amount": self.amount,
            "currency": self.currency
        }
