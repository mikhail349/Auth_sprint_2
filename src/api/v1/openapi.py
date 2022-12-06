import os

import yaml
from flask import Blueprint, render_template

from src.core.config import BASE_DIR


openapi = Blueprint("openapi", __name__)


def render_schema(filename: str) -> str:
    """Ренден html со схемой.

    Args:
        filename: имя файла

    Returns:
        str: сгенерированный html

    """
    SCHEMAS_PATH = os.path.join(BASE_DIR, "src/api/v1/schemas/")
    with open(os.path.join(SCHEMAS_PATH, filename), "r", encoding="utf8") as stream:
        try:
            spec = yaml.safe_load(stream)
            return render_template("swagger.html", spec=spec)
        except yaml.YAMLError:
            return "Error"


@openapi.route("/account", methods=["GET"])
def account():
    return render_schema("openapi_account.yaml")


@openapi.route("/admin", methods=["GET"])
def admin():
    return render_schema("openapi_admin.yaml")
