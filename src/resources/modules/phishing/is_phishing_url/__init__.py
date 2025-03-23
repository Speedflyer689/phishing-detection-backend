import json
from flask import request
from flask_restful import Resource

from library.logger import LOGGER

from .handler import PhishingUrlHandler


class PhishingUrlService(Resource):
    def post(self) -> dict:
        LOGGER.info(f"Checking if the url is phishing or not")
        data = json.loads(request.get_data())
        output = PhishingUrlHandler(data).handle()
        return dict(output)
