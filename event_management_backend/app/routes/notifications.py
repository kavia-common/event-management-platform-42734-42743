from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..db import db
from ..models import Notification

blp = Blueprint("Notifications", "notifications", url_prefix="/api/notifications", description="User notifications")


class NotificationSchema(Schema):
    id = fields.Int()
    message = fields.Str()
    is_read = fields.Bool()
    created_at = fields.DateTime()


@blp.route("/")
class MyNotifications(MethodView):
    @jwt_required()
    @blp.response(200, fields.List(fields.Nested(NotificationSchema)))
    def get(self):
        """List notifications for current user."""
        uid = get_jwt_identity()
        return Notification.query.filter_by(user_id=uid).order_by(Notification.created_at.desc()).all()


@blp.route("/<int:notification_id>/read")
class MarkRead(MethodView):
    @jwt_required()
    @blp.response(200, NotificationSchema)
    def post(self, notification_id: int):
        """Mark a notification as read."""
        uid = get_jwt_identity()
        note = Notification.query.filter_by(id=notification_id, user_id=uid).first_or_404()
        note.is_read = True
        db.session.commit()
        return note
