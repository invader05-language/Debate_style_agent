"""Initial database schema

Revision ID: 001
Revises:
Create Date: 2026-06-04 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial database schema."""

    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("username", sa.String(50), unique=True, nullable=False, index=True),
        sa.Column("email", sa.String(100), unique=True, nullable=False, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # Create debates table
    op.create_table(
        "debates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("topic", sa.String(500), nullable=False),
        sa.Column("status", sa.String(20), default="pending"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("verdict", postgresql.JSONB(), nullable=True),
        sa.Column("action_plan", postgresql.JSONB(), nullable=True),
    )
    op.create_index("ix_debates_status", "debates", ["status"])

    # Create messages table
    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("debate_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("debates.id"), nullable=False),
        sa.Column("round_number", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("model_used", sa.String(50), nullable=False),
        sa.Column("confidence", sa.Float(), default=0.8),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_messages_debate_id", "messages", ["debate_id"])

    # Create memories table
    op.create_table(
        "memories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("topic", sa.String(500), nullable=False),
        sa.Column("debate_summary", sa.Text(), nullable=False),
        sa.Column("outcome", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Float(), default=0.5),
        sa.Column("tags", postgresql.ARRAY(sa.String()), default=[]),
        sa.Column("lessons_learned", postgresql.ARRAY(sa.String()), default=[]),
        sa.Column("embedding", Vector(1024), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_memories_topic", "memories", ["topic"])

    # Create executions table
    op.create_table(
        "executions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("debate_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("debates.id"), nullable=False),
        sa.Column("status", sa.String(20), default="pending"),
        sa.Column("code_generated", sa.Text(), nullable=True),
        sa.Column("execution_result", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_executions_debate_id", "executions", ["debate_id"])
    op.create_index("ix_executions_status", "executions", ["status"])

    # Create HNSW index for vector similarity search on memories
    op.execute(
        "CREATE INDEX ix_memories_embedding ON memories USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table("executions")
    op.drop_table("memories")
    op.drop_table("messages")
    op.drop_table("debates")
    op.drop_table("users")
    op.execute("DROP EXTENSION IF EXISTS vector")
