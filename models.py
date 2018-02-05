from app import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(50), nullable = False)
    body = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, nickname, body, created_at):
        self.nickname = nickname
        self.body = body
        self.created_at = created_at
