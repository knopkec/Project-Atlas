"""Shared test fixtures."""

import os
import tempfile

# Point the app at an isolated SQLite database for the test run, before any
# application module reads the settings.
_tmpdir = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(_tmpdir, 'test.db')}"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
