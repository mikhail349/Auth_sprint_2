from flask import Blueprint

from src.api.v1.oauth.ya import ya


oauth = Blueprint("oauth", __name__, url_prefix="/oauth")
oauth.register_blueprint(ya)