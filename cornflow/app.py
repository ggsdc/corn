import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from .config import app_config
from .endpoints import InstanceEndpoint, InstanceDetailsEndpoint, UserEndpoint, UserDetailsEndpoint, LoginEndpoint, \
    ExecutionEndpoint, ExecutionDetailsEndpoint, ExecutionStatusEndpoint, DAGEndpoint, SignUpEndpoint, InstanceDetailsEndpoint, InstanceFileEndpoint
from .shared.utils import db, bcrypt
from flask_cors import CORS


def create_app(env_name='development'):
    """

    :param str environment:
    :return: the application that is going to be running :class:`Flask`
    :rtype: :class:`Flask`
    """

    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    if env_name == 'development':
        # TODO: not sure if we should keep this line and if so, here.
        CORS(app)
    bcrypt.init_app(app)
    db.init_app(app)
    api = Api(app)
    api.add_resource(InstanceFileEndpoint, '/instancefile/', endpoint="instance-file")
    api.add_resource(InstanceDetailsEndpoint, '/instance/<string:idx>/', endpoint="instances-detail")
    api.add_resource(InstanceEndpoint, '/instance/', endpoint="instance")
    api.add_resource(ExecutionDetailsEndpoint, '/execution/<string:idx>/', endpoint="execution-detail")
    api.add_resource(ExecutionStatusEndpoint, '/execution/status/<string:idx>/', endpoint="execution-status")
    api.add_resource(ExecutionEndpoint, '/execution/', endpoint="execution")
    api.add_resource(DAGEndpoint, '/dag/<string:idx>/', endpoint="dag")
    api.add_resource(UserEndpoint, '/user/', endpoint="user")
    api.add_resource(UserDetailsEndpoint, '/user/<string:user_id>/', endpoint="user-detail")
    api.add_resource(LoginEndpoint, '/login/', endpoint="login")
    api.add_resource(SignUpEndpoint, '/signup/', endpoint="signup")

    return app


if __name__ == '__main__':
    environment_name = os.getenv('FLASK_ENV', 'development')
    # env_name = 'development'
    app = create_app(environment_name)
    app.run()
