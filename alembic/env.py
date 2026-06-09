"""
Alembic environment configuration for Multi-AI Debate Agent.
Supports both online and offline migration modes.
"""

import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import backend config and models
from backend.config import config as backend_config
from backend.database import Base

# Import all models to ensure they are registered with Base.metadata
from backend.models import DebateModel, MessageModel, MemoryModel, ExecutionModel, UserModel

# Alembic Config object
alembic_config = context.config

# Set the database URL from backend config
alembic_config.set_main_option("sqlalchemy.url", backend_config.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
))

# Setup logging from alembic.ini
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Metadata for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Generates SQL scripts without connecting to the database.
    Useful for generating migration scripts for review.
    """
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with the given connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        # Include pgvector extension in migrations
        include_extensions=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine.

    Creates an async engine and runs migrations.
    """
    connectable = async_engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Enable pgvector extension
        await connection.execute(
            __import__('sqlalchemy').text("CREATE EXTENSION IF NOT EXISTS vector")
        )
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Connects to the database and applies migrations.
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
