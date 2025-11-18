from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..db import db
from ..models import Schedule, Event, User

blp = Blueprint("Schedules", "schedules", url_prefix="/api/events/<int:event_id>/schedules", description="Event schedule management")


class ScheduleSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)


@blp.route("/")
class ScheduleList(MethodView):
    @blp.response(200, fields.List(fields.Nested(ScheduleSchema)))
    def get(self, event_id: int):
        """List schedules for an event."""
        Event.query.get_or_404(event_id)
        return Schedule.query.filter_by(event_id=event_id).order_by(Schedule.start_time.asc()).all()

    @jwt_required()
    @blp.arguments(ScheduleSchema)
    @blp.response(201, ScheduleSchema)
    def post(self, data, event_id: int):
        """Create schedule item for event (admin only)."""
        user = User.query.get(get_jwt_identity())
        if not user or not user.is_admin:
            abort(403, message="Admin privileges required")
        Event.query.get_or_404(event_id)
        item = Schedule(event_id=event_id, **data)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/<int:schedule_id>")
class ScheduleDetail(MethodView):
    @blp.response(200, ScheduleSchema)
    def get(self, event_id: int, schedule_id: int):
        """Get schedule item."""
        Event.query.get_or_404(event_id)
        return Schedule.query.filter_by(event_id=event_id, id=schedule_id).first_or_404()

    @jwt_required()
    @blp.arguments(ScheduleSchema(partial=True))
    @blp.response(200, ScheduleSchema)
    def put(self, data, event_id: int, schedule_id: int):
        """Update schedule item (admin only)."""
        user = User.query.get(get_jwt_identity())
        if not user or not user.is_admin:
            abort(403, message="Admin privileges required")
        item = Schedule.query.filter_by(event_id=event_id, id=schedule_id).first_or_404()
        for k, v in data.items():
            setattr(item, k, v)
        db.session.commit()
        return item

    @jwt_required()
    @blp.response(204)
    def delete(self, event_id: int, schedule_id: int):
        """Delete schedule item (admin only)."""
        user = User.query.get(get_jwt_identity())
        if not user or not user.is_admin:
            abort(403, message="Admin privileges required")
        item = Schedule.query.filter_by(event_id=event_id, id=schedule_id).first_or_404()
        db.session.delete(item)
        db.session.commit()
        return ""
