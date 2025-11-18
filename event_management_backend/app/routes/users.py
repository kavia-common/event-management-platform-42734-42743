from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import Schema, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User

blp = Blueprint("Users", "users", url_prefix="/api/users", description="User profile endpoints")


class UserOutSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    name = fields.Str()
    is_admin = fields.Bool()


@blp.route("/me")
class Me(MethodView):
    @jwt_required()
    @blp.response(200, UserOutSchema)
    def get(self):
        """Get current user's profile."""
        uid = get_jwt_identity()
        user = User.query.get_or_404(uid)
        return user
