import os

from flask import Flask
from flask_migrate import Migrate
from werkzeug.utils import import_string

from adapters.google import GoogleOAuth2Adapter
from example.extensions import db
from example.routes import index

ENVIRONMENTS = {
    "production": "example.config.ProductionConfig",
    "local": "example.config.LocalConfig",
    "test": "example.config.TestConfig",
}
settings = import_string(ENVIRONMENTS[os.getenv("FLASK_ENV", "production")])


def initialize_google_adapter(app):
    google_adapter = GoogleOAuth2Adapter(
        client_id=app.config.get("GOOGLE_CLIENT_ID"),
        client_secret=app.config.get("GOOGLE_CLIENT_SECRET"),
        redirect_uri=app.config.get("GOOGLE_REDIRECT_URI"),
        scope=app.config.get("GOOGLE_SCOPES"),
    )

    app.extensions = getattr(app, "extensions", {})
    app.extensions["google_adapter"] = google_adapter
    return app


def create_app(configuration_object=settings):
    app = Flask(__name__)
    app.config.from_object(configuration_object)

    # SQLAlchemy models
    db.init_app(app)

    # Handle model migrations
    migrate = Migrate()
    migrate.init_app(app, db)

    # Init adapter
    app = initialize_google_adapter(app)

    # Routes
    app.register_blueprint(blueprint=index.routes)

    return app


if __name__ == "__main__":
    app = create_app(settings)
    app.run(host="0.0.0.0", port=5000, debug=True)
