"""Shared test fixtures."""

import os
import tempfile

# Point the app at an isolated SQLite database for the test run, before any
# application module reads the settings.
_tmpdir = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(_tmpdir, 'test.db')}"

import pytest
from fastapi.testclient import TestClient

import app.models  # noqa: F401  (register models on Base.metadata)
from app.db import Base, engine
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_db():
    """Start each test with a clean schema and tear it down afterwards."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
