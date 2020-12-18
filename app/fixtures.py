from .models import User, Organization, Repository


def load_fixture_data(session):
    # CREATE USER DATA
    john = User(email="john@beatles.com")
    paul = User(email="paul@beatles.com")
    admin = User(email="admin@admin.com")
    mike = User(email="mike@monsters.com")
    sully = User(email="sully@monsters.com")
    ringo = User(email="ringo@beatles.com")
    randall = User(email="randall@monsters.com")
    users = [
        john,
        paul,
        admin,
        mike,
        sully,
        ringo,
        randall,
    ]
    for user in users:
        session.add(user)

    # CREATE RESOURCE DATA
    beatles = Organization(
        name="The Beatles", billing_address="64 Penny Ln Liverpool, UK"
    )
    monsters = Organization(
        name="Monsters Inc.", billing_address="123 Scarers Rd Monstropolis, USA"
    )
    organizations = [beatles, monsters]
    for org in organizations:
        session.add(org)
    abby_road = Repository(name="Abbey Road", organization=beatles)
    paperwork = Repository(name="Paperwork", organization=monsters)
    repositories = [
        abby_road,
        paperwork,
    ]
    for repo in repositories:
        session.add(repo)

    session.commit()
