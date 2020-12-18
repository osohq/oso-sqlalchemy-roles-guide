from flask import Blueprint, g, request
from .models import User, Organization, Repository

bp = Blueprint("routes", __name__)


@bp.route("/orgs/<int:org_id>/repos", methods=["GET"])
def repos_index(org_id):
    org = g.session.query(Organization).filter(Organization.id == org_id).first()

    repos = g.session.query(Repository).filter(Repository.organization.has(id=org_id))
    return {f"repos": [repo.repr() for repo in repos]}


@bp.route("/orgs/<int:org_id>/billing", methods=["GET"])
def billing_show(org_id):
    org = g.session.query(Organization).filter(Organization.id == org_id).first()
    return {f"billing_address": org.billing_address}
