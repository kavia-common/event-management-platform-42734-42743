"""initial

Revision ID: 0001_initial
Revises:
Create Date: 2025-11-18 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_unique_constraint("uq_users_email", "users", ["email"])

    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=True),
        sa.Column("created_by_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_events_title", "events", ["title"], unique=False)
    op.create_index("ix_events_start_time", "events", ["start_time"], unique=False)

    op.create_table(
        "schedules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_schedules_event_id", "schedules", ["event_id"], unique=False)

    op.create_table(
        "registrations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="registered"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("canceled_at", sa.DateTime(), nullable=True),
    )
    op.create_unique_constraint("uq_user_event", "registrations", ["user_id", "event_id"])
    op.create_index("ix_registrations_user", "registrations", ["user_id"], unique=False)
    op.create_index("ix_registrations_event", "registrations", ["event_id"], unique=False)

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("message", sa.String(length=500), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_notifications_user", "notifications", ["user_id"], unique=False)


def downgrade():
    op.drop_index("ix_notifications_user", table_name="notifications")
    op.drop_table("notifications")
    op.drop_index("ix_registrations_event", table_name="registrations")
    op.drop_index("ix_registrations_user", table_name="registrations")
    op.drop_constraint("uq_user_event", "registrations", type_="unique")
    op.drop_table("registrations")
    op.drop_index("ix_schedules_event_id", table_name="schedules")
    op.drop_table("schedules")
    op.drop_index("ix_events_start_time", table_name="events")
    op.drop_index("ix_events_title", table_name="events")
    op.drop_table("events")
    op.drop_constraint("uq_users_email", "users", type_="unique")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
