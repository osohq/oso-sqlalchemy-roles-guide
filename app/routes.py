from flask import Blueprint, g, request, current_app
from flask_oso import authorize
from .models import User, Organization, Repository, OrganizationRole
from .db import Session

from sqlalchemy_oso import roles as oso_roles

bp = Blueprint("routes", __name__)


@bp.route("/")
def index():
    if "current_user" in g:
        return g.current_user.repr()
    else:
        return f'Please "log in"'


@bp.route("/orgs", methods=["GET"])
def orgs_index():
    orgs = g.auth_session.query(Organization).all()
    return {"orgs": [org.repr() for org in orgs]}


@bp.route("/orgs/<int:org_id>/repos", methods=["GET"])
def repos_index(org_id):
    org = g.basic_session.query(Organization).filter(Organization.id == org_id).first()
    current_app.oso.authorize(org, actor=g.current_user, action="LIST_REPOS")

    repos = g.basic_session.query(Repository).filter(
        Repository.organization.has(id=org_id)
    )
    return {f"repos": [repo.repr() for repo in repos]}


@bp.route("/orgs/<int:org_id>/billing", methods=["GET"])
def billing_show(org_id):
    org = g.basic_session.query(Organization).filter(Organization.id == org_id).first()
    current_app.oso.authorize(org, actor=g.current_user, action="READ_BILLING")
    return {f"billing_address": org.billing_address}


@bp.route("/orgs/<int:org_id>/roles", methods=["GET"])
def org_roles_index(org_id):
    # Get authorized roles for this organization
    org = g.basic_session.query(Organization).filter_by(id=org_id).first()
    current_app.oso.authorize(org, actor=g.current_user, action="LIST_ROLES")

    roles = oso_roles.get_resource_roles(g.auth_session, org)
    return {
        f"roles": [{"user": role.user.repr(), "role": role.repr()} for role in roles]
    }
