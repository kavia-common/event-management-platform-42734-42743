from datetime import datetime
from sqlalchemy import UniqueConstraint, Index
from ..db import db


class Registration(db.Model):
    """Registration of a user to an event."""

    __tablename__ = "registrations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    status = db.Column(db.String(32), default="registered", nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    canceled_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="registrations")
    event = db.relationship("Event", back_populates="registrations")

    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="uq_user_event"),
        Index("ix_registrations_user", "user_id"),
        Index("ix_registrations_event", "event_id"),
    )
