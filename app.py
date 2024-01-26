import mongoengine
from flask import Flask

from app.blueprint_register import setup_blueprints


def create_app() -> Flask:
    flask_app = Flask(__name__)

    DB_NAME = "test_db"
    mongoengine.connect(host=f"mongodb://localhost:27017/{DB_NAME}")

    with flask_app.app_context():
        setup_blueprints()

    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
