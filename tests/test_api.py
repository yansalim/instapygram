"""
Basic integration tests for the Pipegram Flask API.

These tests cover error scenarios such as missing JSON payloads,
missing required fields and absence of an admin token. They ensure
that the decorator logic and request validation behave as expected.
"""
from flask import json


def test_status_requires_username(client):
    # When no username is provided, a BadRequest (400) should be raised
    resp = client.get("/auth/status")
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "Bad Request"


def test_login_requires_fields(client):
    # Missing username and password should return 400
    resp = client.post("/auth/login", json={})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "Bad Request"


def test_protected_route_without_token(client):
    # Protected endpoint should return 401 if no Authorization header is present
    payload = {"username": "testuser", "caption": "Hello", "url": "https://example.com/image.jpg"}
    resp = client.post("/post/photo-feed", json=payload)
    assert resp.status_code == 401
    data = resp.get_json()
    # Should be unauthorized error
    assert data["error"] == "Unauthorized"