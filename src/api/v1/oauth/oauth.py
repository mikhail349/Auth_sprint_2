from flask import Blueprint

from src.api.v1.oauth.ya import ya
from src.api.v1.oauth.google import google


oauth = Blueprint("oauth", __name__, url_prefix="/oauth")
oauth.register_blueprint(ya)
oauth.register_blueprint(google)
