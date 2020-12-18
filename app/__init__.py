from flask import g, Flask, request

from datetime import datetime, timedelta

from .models import Base
from .fixtures import load_fixture_data
from .db import engine, Session
from .authorization import init_oso


def create_app():
    app = Flask(__name__)
    init_oso(app)

    Base.metadata.create_all(engine)

    session = Session()
    load_fixture_data(session)

    from . import routes

    app.register_blueprint(routes.bp)

    return app
