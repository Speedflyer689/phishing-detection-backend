from typing import Dict, Type
from flask_restful import Resource
from library.api import APIOutput

from .phishing.controller import phishing_factory
from .reporting.controller import reporting_factory

class Base(Resource):
    def get(self) -> dict:
        return APIOutput.success(data={}, message="Base url successfully called")


service_factory: Dict[str, Type[Resource]] = {
    "/": Base,
}

service_factory.update(phishing_factory)
service_factory.update(reporting_factory)