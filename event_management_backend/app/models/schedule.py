from datetime import datetime
from ..db import db


class Schedule(db.Model):
    """Scheduled agenda items for an event."""

    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    event = db.relationship("Event", back_populates="schedules")
