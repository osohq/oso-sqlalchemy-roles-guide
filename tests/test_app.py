from .conftest import test_client, test_db_session
from flask import json
import pytest

from app.models import User


def test_db_loads(test_db_session):
    just_john = (
        test_db_session.query(User).filter(User.email == "john@beatles.com").all()
    )
    assert len(just_john) == 1


def test_user(test_client):
    resp = test_client.get("/")
    assert resp.status_code == 401

    resp = test_client.get("/", headers={"user": "john@beatles.com"})
    assert resp.status_code == 200
    assert json.loads(resp.data).get("email") == "john@beatles.com"


def test_orgs(test_client):
    resp = test_client.get("/orgs", headers={"user": "john@beatles.com"})
    assert resp.status_code == 200

    resp = test_client.get("/orgs", headers={"user": "mike@monsters.com"})
    assert resp.status_code == 200


def test_repos_index(test_client):
    resp = test_client.get("/orgs/1/repos", headers={"user": "john@beatles.com"})
    assert resp.status_code == 200


def test_billing_show(test_client):
    resp = test_client.get("/orgs/1/billing", headers={"user": "john@beatles.com"})
    assert resp.status_code == 200
