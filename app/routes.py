from flask import Blueprint, g, request, current_app
from flask_oso import authorize
from .models import User, Organization, Repository
from .db import Session

bp = Blueprint("routes", __name__)


@bp.route("/")
def index():
    if "current_user" in g:
        return g.current_user.repr()
    else:
        return f'Please "log in"'


@bp.route("/orgs", methods=["GET"])
def orgs_index():
    orgs = g.basic_session.query(Organization).all()
    return {"orgs": [org.repr() for org in orgs]}


@bp.route("/orgs/<int:org_id>/repos", methods=["GET"])
def repos_index(org_id):
    org = g.basic_session.query(Organization).filter(Organization.id == org_id).first()

    repos = g.basic_session.query(Repository).filter(
        Repository.organization.has(id=org_id)
    )
    return {f"repos": [repo.repr() for repo in repos]}


@bp.route("/orgs/<int:org_id>/billing", methods=["GET"])
def billing_show(org_id):
    org = g.basic_session.query(Organization).filter(Organization.id == org_id).first()
    return {f"billing_address": org.billing_address}
