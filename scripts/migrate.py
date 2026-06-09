"""
Database migration management script for Multi-AI Debate Agent.

Usage:
    python scripts/migrate.py upgrade     # Apply all pending migrations
    python scripts/migrate.py downgrade   # Revert last migration
    python scripts/migrate.py revision    # Create a new migration
    python scripts/migrate.py current     # Show current revision
    python scripts/migrate.py history     # Show migration history
    python scripts/migrate.py check       # Check for model changes
"""

import subprocess
import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_alembic(*args: str) -> int:
    """Run alembic command with given arguments."""
    cmd = [sys.executable, "-m", "alembic"] + list(args)
    return subprocess.run(cmd, cwd=project_root).returncode


def upgrade(revision: str = "head") -> None:
    """Apply migrations up to given revision."""
    print(f"Upgrading database to {revision}...")
    sys.exit(run_alembic("upgrade", revision))


def downgrade(revision: str = "-1") -> None:
    """Revert migrations to given revision."""
    print(f"Downgrading database to {revision}...")
    sys.exit(run_alembic("downgrade", revision))


def revision(message: str = "auto") -> None:
    """Create a new migration revision."""
    if message == "auto":
        print("Creating auto-generated migration...")
        sys.exit(run_alembic("revision", "--autogenerate", "-m", "auto_generated"))
    else:
        print(f"Creating migration: {message}")
        sys.exit(run_alembic("revision", "-m", message))


def current() -> None:
    """Show current database revision."""
    sys.exit(run_alembic("current", "-v"))


def history() -> None:
    """Show migration history."""
    sys.exit(run_alembic("history", "-v"))


def check() -> None:
    """Check for model changes that need migration."""
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "check"],
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("Database is up to date with models.")
    else:
        print("Database needs migration:")
        print(result.stderr)
    sys.exit(result.returncode)


if __name__ == "__main__":
    commands = {
        "upgrade": upgrade,
        "downgrade": downgrade,
        "revision": revision,
        "current": current,
        "history": history,
        "check": check,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print(__doc__)
        print(f"Available commands: {', '.join(commands.keys())}")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    commands[cmd](*args)
