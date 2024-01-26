from flask import current_app as app

from app.blueprint import v1_blueprint


def setup_blueprints():
    app.register_blueprint(v1_blueprint)