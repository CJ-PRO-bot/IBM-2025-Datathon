# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(16), default="user")  # "user" or "admin"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='submissions')
    report_type = db.Column(db.String(32), default="illegal_dumping")
    image_path = db.Column(db.String(256), nullable=False)

    # AI fields (nullable for backward compatibility)
    ai_label = db.Column(db.String(32))
    ai_score = db.Column(db.Float)
    status = db.Column(db.String(16), default="RECHECK")  # AUTO_OK | RECHECK

    # New smart-verifier fields (safe to leave null)
    phash = db.Column(db.String(32), index=True)
    duplicate_of = db.Column(db.Integer)  # Submission.id if near-duplicate
    exif_time_ok = db.Column(db.Boolean)
    action_score = db.Column(db.Float)
    auth_score = db.Column(db.Float)          # authenticity (0..1)
    relevance_score = db.Column(db.Float)     # waste/cleanup relevance (0..1)
    model_version = db.Column(db.String(32))  # e.g., "legacy" or "smart_v1"

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submission = db.relationship('Submission', backref='messages')
    sender = db.relationship('User')
