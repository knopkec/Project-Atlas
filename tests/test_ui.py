"""Tests for the UI: the root route serves the page and static assets load."""

from tests.conftest import client


def test_index_serves_html():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "OWC" in resp.text


def test_static_assets_are_served():
    css = client.get("/static/style.css")
    assert css.status_code == 200
    js = client.get("/static/app.js")
    assert js.status_code == 200
