from flask import g, Flask, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, User
from .fixtures import load_fixture_data

from werkzeug.exceptions import Unauthorized

from flask_oso import FlaskOso
from oso import Oso
from sqlalchemy_oso import register_models, set_get_session


engine = create_engine("sqlite:///roles.db")
Session = sessionmaker(bind=engine)


def create_app():
    app = Flask(__name__)

    init_oso(app)

    Base.metadata.create_all(engine)

    session = Session()
    load_fixture_data(session)

    from . import routes

    app.register_blueprint(routes.bp)

    @app.before_request
    def set_current_user_and_session():
        if "current_user" not in g:
            email = request.headers.get("user")
            if not email:
                return Unauthorized("user not found")
            try:
                # Set basic (non-auth) session for this request
                g.session = Session()

                # Set user for this request
                g.current_user = (
                    g.session.query(User).filter(User.email == email).first()
                )
            except Exception as e:
                return Unauthorized("user not found")

    return app


base_oso = Oso()
oso = FlaskOso(base_oso)


def init_oso(app):
    register_models(base_oso, Base)
    set_get_session(base_oso, lambda: g.session)
    base_oso.load_file("app/authorization.polar")
    app.oso = oso