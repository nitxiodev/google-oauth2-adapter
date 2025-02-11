from flask import Blueprint

from example.routes.auth import auth
from example.routes.google_api import google

routes = Blueprint("index", __name__, url_prefix="/")

# Nested blueprints
routes.register_blueprint(auth, url_prefix="/")
routes.register_blueprint(google, url_prefix="/google")
