from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..db import db
from ..models import Registration, Event, User

blp = Blueprint("Registrations", "registrations", url_prefix="/api/registrations", description="Registration endpoints")


class RegistrationSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    event_id = fields.Int()
    status = fields.Str()
    created_at = fields.DateTime()
    canceled_at = fields.DateTime(allow_none=True)


class RegisterRequest(Schema):
    event_id = fields.Int(required=True)


@blp.route("/")
class MyRegistrations(MethodView):
    @jwt_required()
    @blp.response(200, fields.List(fields.Nested(RegistrationSchema)))
    def get(self):
        """List my registrations."""
        uid = get_jwt_identity()
        return Registration.query.filter_by(user_id=uid).all()

    @jwt_required()
    @blp.arguments(RegisterRequest)
    @blp.response(201, RegistrationSchema)
    def post(self, args):
        """Register current user to an event."""
        uid = get_jwt_identity()
        event = Event.query.get_or_404(args["event_id"])
        reg = Registration.query.filter_by(user_id=uid, event_id=event.id).first()
        if reg:
            abort(409, message="Already registered")
        reg = Registration(user_id=uid, event_id=event.id, status="registered")
        db.session.add(reg)
        db.session.commit()
        return reg


@blp.route("/<int:registration_id>/cancel")
class CancelRegistration(MethodView):
    @jwt_required()
    @blp.response(200, RegistrationSchema)
    def post(self, registration_id: int):
        """Cancel my registration."""
        uid = get_jwt_identity()
        reg = Registration.query.get_or_404(registration_id)
        if reg.user_id != uid:
            abort(403, message="Cannot cancel others' registrations")
        reg.status = "canceled"
        reg.canceled_at = datetime.utcnow()
        db.session.commit()
        return reg


@blp.route("/by-event/<int:event_id>")
class AdminListByEvent(MethodView):
    @jwt_required()
    @blp.response(200, fields.List(fields.Nested(RegistrationSchema)))
    def get(self, event_id: int):
        """Admin: list registrations by event."""
        user = User.query.get(get_jwt_identity())
        if not user or not user.is_admin:
            abort(403, message="Admin privileges required")
        Event.query.get_or_404(event_id)
        return Registration.query.filter_by(event_id=event_id).all()
