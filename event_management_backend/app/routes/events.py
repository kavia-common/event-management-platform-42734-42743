from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..db import db
from ..models import Event, User

blp = Blueprint("Events", "events", url_prefix="/api/events", description="Event browsing and management")


class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    location = fields.Str()
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    capacity = fields.Int(allow_none=True)


class EventListQuery(Schema):
    q = fields.Str(load_default=None, description="Search query")
    page = fields.Int(load_default=1)
    per_page = fields.Int(load_default=10)


@blp.route("/")
class EventsList(MethodView):
    @blp.arguments(EventListQuery, location="query")
    @blp.response(200, schema=Schema.from_dict({"items": fields.List(fields.Nested(EventSchema)), "total": fields.Int()})())
    def get(self, args):
        """List events with optional search and pagination."""
        q = args.get("q")
        page = args.get("page", 1)
        per_page = min(args.get("per_page", 10), 50)
        query = Event.query
        if q:
            like = f"%{q}%"
            query = query.filter(Event.title.ilike(like))
        pagination = query.order_by(Event.start_time.asc()).paginate(page=page, per_page=per_page, error_out=False)
        return {"items": [e for e in pagination.items], "total": pagination.total}

    @jwt_required()
    @blp.arguments(EventSchema)
    @blp.response(201, EventSchema)
    def post(self, data):
        """Create a new event (admin only)."""
        user = User.query.get(get_jwt_identity())
        if not user or not user.is_admin:
            abort(403, message="Admin privileges required")
        event = Event(**data, created_by=user)
        db.session.add(event)
        db.session.commit()
        return event


@blp.route("/<int:event_id>")
class EventDetail(MethodView):
    @blp.response(200, EventSchema)
    def get(self, event_id: int):
        """Get event details by id."""
        return Event.query.get_or_404(event_id)

    @jwt_required()
    @blp.arguments(EventSchema(partial=True))
    @blp.response(200, EventSchema)
    def put(self, data, event_id: int):
        """Update an event (admin only)."""
        user = User.query.get(get_jwt_identity())
        if not user or not user.is_admin:
            abort(403, message="Admin privileges required")
        event = Event.query.get_or_404(event_id)
        for k, v in data.items():
            setattr(event, k, v)
        db.session.commit()
        return event

    @jwt_required()
    @blp.response(204)
    def delete(self, event_id: int):
        """Delete an event (admin only)."""
        user = User.query.get(get_jwt_identity())
        if not user or not user.is_admin:
            abort(403, message="Admin privileges required")
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return ""
