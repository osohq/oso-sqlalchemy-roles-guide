from .conftest import test_client, test_db_session
import pytest

from app.models import User


def test_db_loads(test_db_session):
    just_john = (
        test_db_session.query(User).filter(User.email == "john@beatles.com").all()
    )
    assert len(just_john) == 1


def test_org_roles_new(test_client, test_db_session):
    resp = test_client.post(
        "/orgs/1/roles",
        headers={"user": "john@beatles.com"},
        json={"name": "BILLING", "user_email": "ringo@beatles.com"},
    )
    assert resp.status_code == 200

    ringo = test_db_session.query(User).filter_by(email="ringo@beatles.com").first()
    assert ringo.organization_roles[0].name == "BILLING"

    resp = test_client.post(
        "/orgs/1/roles",
        headers={"user": "paul@beatles.com"},
        json={"name": "OWNER", "user_email": "paul@beatles.com"},
    )
    assert resp.status_code == 403


def test_repos_index(test_client):
    resp = test_client.get("/orgs/1/repos", headers={"user": "john@beatles.com"})
    assert resp.status_code == 200


def test_billing_show(test_client):
    resp = test_client.get("/orgs/1/billing", headers={"user": "john@beatles.com"})
    assert resp.status_code == 200
