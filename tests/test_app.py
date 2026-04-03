import json
from app import app


def test_health_check():
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200
    assert r.json["status"] == "ok"


def test_get_members():
    client = app.test_client()
    r = client.get("/members")
    assert r.status_code == 200
    assert isinstance(r.json, list)


def test_post_member_success():
    client = app.test_client()
    payload = {"name": "Charlie", "plan": "Premium", "workouts": ["cardio"]}
    r = client.post("/members", json=payload)
    assert r.status_code == 201
    assert r.json["name"] == "Charlie"


def test_post_member_validation_error():
    client = app.test_client()
    payload = {"name": "Dave"}
    r = client.post("/members", json=payload)
    assert r.status_code == 400


def test_get_metrics():
    client = app.test_client()
    r = client.get("/metrics")
    assert r.status_code == 200
    data = r.json
    assert "members_count" in data
    assert "workouts_count" in data
