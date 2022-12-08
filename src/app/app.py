from flask import Flask, Blueprint, request
from flask_migrate import Migrate
from flask_restful import Api
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from src.api.v1 import user
from src.api.v1.openapi import openapi
from src.api.v1.oauth.oauth import oauth

from src.core.config import redis_settings
from src.api.v1.perms import Permissions
from src.api.v1.roles import Roles
from src.db.db import db, init_db
from src.app.commands import init_commands
from src.services.jwt import init_jwt
from src.utils.jaeger_tracing import configure_tracer


BASE_API_URL = "/api/v1"

configure_tracer()

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

# redis
app.config.from_mapping(redis_settings.uppercased_dict())

# jwt
init_jwt(app)

#jaeger
FlaskInstrumentor().instrument_app(app)

# blueprints
root = Blueprint(BASE_API_URL, __name__, url_prefix=BASE_API_URL)
root.register_blueprint(user)
root.register_blueprint(openapi)
root.register_blueprint(oauth)
app.register_blueprint(root)


api = Api(app)
api.add_resource(Permissions, f"{BASE_API_URL}/perms", f"{BASE_API_URL}/perms/<string:obj_id>")
api.add_resource(Roles, f"{BASE_API_URL}/roles", f"{BASE_API_URL}/roles/<string:obj_id>")

migrate = Migrate(app, db)
init_commands(app)
init_db(app)


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id and not app.debug:
        raise RuntimeError('request id is required')


if __name__ == "__main__":
    app.run(debug=True)
