from datetime import datetime
from passlib.hash import bcrypt
from sqlalchemy import Index
from ..db import db


class User(db.Model):
    """User model representing application users."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    registrations = db.relationship("Registration", back_populates="user", cascade="all, delete-orphan")
    notifications = db.relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_users_email", "email"),
    )

    def set_password(self, password: str) -> None:
        """Hash and set the user's password."""
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        """Verify the password against the stored hash."""
        return bcrypt.verify(password, self.password_hash)
