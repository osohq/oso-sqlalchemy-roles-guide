from .models import User, Organization, Repository, OrganizationRole


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
    beatles = Organization(name="The Beatles")
    monsters = Organization(name="Monsters Inc.")
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

    # CREATE ROLE DATA
    roles = [
        OrganizationRole(
            name="OWNER",
            organization=beatles,
            user=john,
        ),
        OrganizationRole(
            name="MEMBER",
            organization=beatles,
            user=paul,
        ),
        OrganizationRole(
            name="MEMBER",
            organization=beatles,
            user=ringo,
        ),
        OrganizationRole(
            name="OWNER",
            organization=monsters,
            user=mike,
        ),
        OrganizationRole(
            name="MEMBER",
            organization=monsters,
            user=sully,
        ),
        OrganizationRole(
            name="MEMBER",
            organization=monsters,
            user=randall,
        ),
    ]

    for role in roles:
        session.add(role)

    session.commit()
