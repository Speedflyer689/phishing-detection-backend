import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from library.config import Config
from library.flask import handle_generic_exception, handle_400, handle_pydantic_validation_errors

from resources.modules.controller import service_factory

from pydantic import ValidationError

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
api = Api(app)

app.register_error_handler(ValidationError, handle_pydantic_validation_errors)
app.register_error_handler(400, handle_400)
app.register_error_handler(Exception, handle_generic_exception)

with app.app_context():
    # db.init_app(app)
    for path, service in service_factory.items():
        api.add_resource(service, path)

if __name__ == "__main__":
    app.run(port=5000)