from flask import Blueprint, g, request, current_app
from .models import User, Organization, Repository

bp = Blueprint("routes", __name__)


@bp.route("/")
def whoami():
    return f"Hello {g.current_user.email}"


@bp.route("/orgs/<int:org_id>/repos", methods=["GET"])
def repos_index(org_id):
    org = g.session.query(Organization).filter(Organization.id == org_id).first()
    current_app.oso.authorize(org, actor=g.current_user, action="LIST_REPOS")

    repos = g.session.query(Repository).filter_by(organization=org)
    return {f"repos": [repo.repr() for repo in repos]}


@bp.route("/orgs/<int:org_id>/billing", methods=["GET"])
def billing_show(org_id):
    org = g.session.query(Organization).filter(Organization.id == org_id).first()
    current_app.oso.authorize(org, actor=g.current_user, action="READ_BILLING")
    return {f"billing_address": org.billing_address}
