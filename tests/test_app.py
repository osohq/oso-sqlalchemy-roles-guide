from .conftest import test_client, test_db_session
from flask import json
import pytest

from app.models import User, Repository


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

    orgs = json.loads(resp.data).get("orgs")
    assert len(orgs) == 1
    assert orgs[0]["name"] == "The Beatles"

    resp = test_client.get("/orgs", headers={"user": "mike@monsters.com"})
    assert resp.status_code == 200

    orgs = json.loads(resp.data).get("orgs")
    assert len(orgs) == 1
    assert orgs[0]["name"] == "Monsters Inc."


def test_repos_index(test_client):
    resp = test_client.get("/orgs/1/repos", headers={"user": "john@beatles.com"})
    assert resp.status_code == 200

    repos = json.loads(resp.data).get("repos")
    assert len(repos) == 1
    assert repos[0]["name"] == "Abbey Road"

    resp = test_client.get("/orgs/2/repos", headers={"user": "john@beatles.com"})
    assert resp.status_code == 403


def test_billing_show(test_client):
    resp = test_client.get("/orgs/1/billing", headers={"user": "john@beatles.com"})
    assert resp.status_code == 200

    resp = test_client.get("/orgs/1/billing", headers={"user": "paul@beatles.com"})
    assert resp.status_code == 403


def test_org_roles(test_client):
    resp = test_client.get("/orgs/1/roles", headers={"user": "john@beatles.com"})
    roles = json.loads(resp.data).get("roles")
    assert resp.status_code == 200
    assert len(roles) == 3
    assert roles[0].get("user").get("email") == "john@beatles.com"
    assert roles[1].get("user").get("email") == "paul@beatles.com"
    assert roles[2].get("user").get("email") == "ringo@beatles.com"

    resp = test_client.get("/orgs/1/roles", headers={"user": "paul@beatles.com"})
    assert resp.status_code == 403

    resp = test_client.get("/orgs/2/roles", headers={"user": "john@beatles.com"})
    assert resp.status_code == 403
