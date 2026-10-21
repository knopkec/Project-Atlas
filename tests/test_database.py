"""Database foundation tests: connectivity and pgvector extension."""

from sqlalchemy import text

from app.db import engine


def test_database_is_reachable():
    with engine.connect() as conn:
        assert conn.execute(text("SELECT 1")).scalar() == 1


def test_pgvector_extension_is_enabled():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
        )
        assert result.scalar() == 1
