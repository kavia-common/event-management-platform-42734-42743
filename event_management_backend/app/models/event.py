from datetime import datetime
from sqlalchemy import Index
from ..db import db


class Event(db.Model):
    """Event model representing an event that users can register for."""

    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=True)

    created_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_by = db.relationship("User", backref="events_created")

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    schedules = db.relationship("Schedule", back_populates="event", cascade="all, delete-orphan")
    registrations = db.relationship("Registration", back_populates="event", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_events_title", "title"),
        Index("ix_events_start_time", "start_time"),
    )
