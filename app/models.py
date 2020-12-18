import json
import datetime
from enum import Enum

from flask import current_app
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.schema import Table, Column, ForeignKey
from sqlalchemy.orm import relationship, scoped_session, backref

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_oso import authorized_sessionmaker
from sqlalchemy_utils.types.choice import ChoiceType

from sqlalchemy_oso.roles import resource_role_class


Base = declarative_base()

## MODELS ##


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String())

    def repr(self):
        return {"id": self.id, "name": self.name}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String())

    def repr(self):
        return {"id": self.id, "email": self.email}


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True)
    name = Column(String(256))

    # many-to-one relationship with organizations
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", backref="repositories", lazy=True)

    def repr(self):
        return {"id": self.id, "name": self.name}


## ROLE MODELS ##

OrganizationRoleMixin = resource_role_class(
    Base, User, Organization, ["OWNER", "MEMBER", "BILLING"]
)


class OrganizationRole(Base, OrganizationRoleMixin):
    def repr(self):
        return {"id": self.id, "name": str(self.name)}
