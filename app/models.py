from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Operator') # 'Admin' or 'Operator'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    records = db.relationship('Record', backref='owner', foreign_keys='Record.user_id', lazy=True)
    confirmed_records = db.relationship('Record', backref='confirmed_by', foreign_keys='Record.confirmed_by_id', lazy=True)

    def is_admin(self):
        return self.role == 'Admin'

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    confirmed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    audio_file_path = db.Column(db.String(255), nullable=False)
    raw_text = db.Column(db.Text)
    corrected_text = db.Column(db.Text)
    
    command = db.Column(db.String(100))
    identifier = db.Column(db.String(100))
    
    status = db.Column(db.String(20), default='pending') # 'pending', 'confirmed'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
