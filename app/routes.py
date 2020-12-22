from flask import Blueprint, g, request, current_app
from .models import User, Organization, Repository

from sqlalchemy_oso.roles import add_user_role, reassign_user_role

bp = Blueprint("routes", __name__)


@bp.route("/")
def whoami():
    return f"Hello {g.current_user.email}"


@bp.route("/orgs/<int:org_id>/repos", methods=["GET"])
def repos_index(org_id):
    org = g.session.query(Organization).filter_by(id=org_id).first()
    current_app.oso.authorize(org, actor=g.current_user, action="LIST_REPOS")

    repos = g.session.query(Repository).filter_by(organization=org)
    return {f"repos": [repo.repr() for repo in repos]}


@bp.route("/orgs/<int:org_id>/billing", methods=["GET"])
def billing_show(org_id):
    org = g.session.query(Organization).filter_by(id=org_id).first()
    current_app.oso.authorize(org, actor=g.current_user, action="READ_BILLING")
    return {f"billing_address": org.billing_address}


@bp.route("/orgs/<int:org_id>/roles", methods=["POST"])
def org_roles_new(org_id):
    org = g.session.query(Organization).filter_by(id=org_id).first()
    current_app.oso.authorize(org, actor=g.current_user, action="CREATE_ROLE")

    # Create role
    role_name = request.get_json().get("name")
    user_email = request.get_json().get("user_email")
    user = g.session.query(User).filter_by(email=user_email).first()
    try:
        add_user_role(g.session, user, org, role_name, commit=True)
    except Exception as e:
        reassign_user_role(g.session, user, org, role_name)

    return f"created a new role for org: {org_id}, {user_email}, {role_name}"
