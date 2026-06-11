"""Add v2.0 tables: ai_models, tasks, task_messages, user_settings, api_keys, faqs, notifications

Revision ID: 002
Revises: 001
Create Date: 2026-06-09 15:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- AI Models table ---
    op.create_table(
        "ai_models",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("model_id", sa.String(100), nullable=False),
        sa.Column("api_url", sa.String(500), nullable=False),
        sa.Column("api_key", sa.String(500), nullable=False),
        sa.Column("api_format", sa.String(20), default="openai"),
        sa.Column("max_tokens", sa.Integer(), default=4096),
        sa.Column("temperature", sa.Float(), default=0.7),
        sa.Column("is_preset", sa.Boolean(), default=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("icon", sa.String(50), nullable=True),
        sa.Column("color", sa.String(20), nullable=True),
        sa.Column("last_tested_at", sa.DateTime(), nullable=True),
        sa.Column("last_test_status", sa.String(20), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_ai_models_name", "ai_models", ["name"])
    op.create_index("ix_ai_models_provider", "ai_models", ["provider"])

    # --- Tasks table ---
    op.create_table(
        "tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("type", sa.String(20), nullable=False),  # debate / think
        sa.Column("topic", sa.String(500), nullable=False),
        sa.Column("status", sa.String(20), default="pending"),
        sa.Column("config", postgresql.JSONB(), nullable=True),
        sa.Column("result", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_tasks_type", "tasks", ["type"])
    op.create_index("ix_tasks_status", "tasks", ["status"])

    # --- Task Messages table ---
    op.create_table(
        "task_messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("task_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tasks.id"), nullable=False),
        sa.Column("model_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("ai_models.id"), nullable=True),
        sa.Column("role", sa.String(30), nullable=False),  # pro/con/judge/thinker/synthesizer/user/system
        sa.Column("round_number", sa.Integer(), default=1),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("structured", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_task_messages_task_id", "task_messages", ["task_id"])

    # --- User Settings table ---
    op.create_table(
        "user_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("language", sa.String(10), default="zh"),
        sa.Column("theme_mode", sa.String(10), default="light"),
        sa.Column("notifications", sa.Boolean(), default=True),
        sa.Column("weekly_digest", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index("ix_user_settings_user_id", "user_settings", ["user_id"])

    # --- API Keys table ---
    op.create_table(
        "api_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("api_key_enc", sa.Text(), nullable=False),
        sa.Column("key_preview", sa.String(20), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # --- FAQs table ---
    op.create_table(
        "faqs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("question", sa.String(500), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("category", sa.String(50), nullable=True),
        sa.Column("sort_order", sa.Integer(), default=0),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_faqs_category", "faqs", ["category"])

    # --- Notifications table ---
    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("type", sa.String(20), default="info"),
        sa.Column("is_read", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_notifications_is_read", "notifications", ["is_read"])


def downgrade() -> None:
    op.drop_table("notifications")
    op.drop_table("faqs")
    op.drop_table("api_keys")
    op.drop_table("user_settings")
    op.drop_table("task_messages")
    op.drop_table("tasks")
    op.drop_table("ai_models")
