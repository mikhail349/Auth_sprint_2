from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from src.api.v1 import user
from src.api.v1.openapi import openapi
from src.app.extensions import jwt

from src.core.config import jwt_settings, redis_settings
from src.api.v1.perms import Permissions
from src.api.v1.roles import Roles
from src.db.db import db, init_db
from src.app.commands import init_commands


BASE_API_URL = "/api/v1/"

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# redis
app.config.from_mapping(redis_settings.uppercased_dict())

# jwt
app.config.from_mapping(jwt_settings.uppercased_dict())
jwt.init_app(app)

# blueprints
app.register_blueprint(user, url_prefix=f"{BASE_API_URL}user")
app.register_blueprint(openapi, url_prefix=f"{BASE_API_URL}openapi")


api = Api(app)
api.add_resource(Permissions, f"{BASE_API_URL}perms", f"{BASE_API_URL}perms/<string:obj_id>")
api.add_resource(Roles, f"{BASE_API_URL}roles", f"{BASE_API_URL}roles/<string:obj_id>")

migrate = Migrate(app, db)
init_commands(app)
init_db(app)


if __name__ == "__main__":
    app.run()
