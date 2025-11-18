from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields, validate
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from ..db import db
from ..models import User


blp = Blueprint(
    "Auth",
    "auth",
    url_prefix="/api/auth",
    description="Authentication endpoints for registration and login",
)


class RegisterSchema(Schema):
    email = fields.Email(required=True, description="Email address")
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6, max=255))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class TokenSchema(Schema):
    access_token = fields.Str(required=True)
    refresh_token = fields.Str(required=True)


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(RegisterSchema, location="json")
    @blp.response(201, TokenSchema)
    def post(self, args):
        """Register a new user and return JWT tokens."""
        email = args["email"].lower()
        if User.query.filter_by(email=email).first():
            abort(409, message="Email already registered")
        user = User(email=email, name=args["name"])
        user.set_password(args["password"])
        db.session.add(user)
        db.session.commit()
        access = create_access_token(identity=user.id)
        refresh = create_refresh_token(identity=user.id)
        return {"access_token": access, "refresh_token": refresh}


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginSchema, location="json")
    @blp.response(200, TokenSchema)
    def post(self, args):
        """Login with email and password and receive access/refresh tokens."""
        email = args["email"].lower()
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(args["password"]):
            abort(401, message="Invalid credentials")
        access = create_access_token(identity=user.id)
        refresh = create_refresh_token(identity=user.id)
        return {"access_token": access, "refresh_token": refresh}


@blp.route("/refresh")
class Refresh(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, schema=Schema.from_dict({"access_token": fields.Str(required=True)})())
    def post(self):
        """Refresh an access token using a refresh token."""
        uid = get_jwt_identity()
        access = create_access_token(identity=uid)
        return {"access_token": access}


@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    @blp.response(200, schema=Schema.from_dict({"message": fields.Str()})())
    def post(self):
        """Logout endpoint (stateless; client should discard tokens)."""
        return {"message": "Logged out"}
