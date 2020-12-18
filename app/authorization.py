from flask import current_app, g, request
from werkzeug.exceptions import Unauthorized

from sqlalchemy.orm import Session

from .db import engine, Session
from .models import Base, User

def init_oso(app):
    @app.before_request
    def set_current_user():
        if "current_user" not in g:
            email = request.headers.get("user")
            if not email:
                return Unauthorized("user not found")
            try:
                basic_session = Session()
                g.basic_session = basic_session
                g.current_user = (
                    basic_session.query(User).filter(User.email == email).first()
                )
            except Exception as e:
                return Unauthorized("user not found")
