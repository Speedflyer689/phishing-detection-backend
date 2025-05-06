import json
from flask import request
from flask_restful import Resource

from library.logger import LOGGER

from .handler import ReportIncidentHandler


class ReportIncidentService(Resource):
    def post(self) -> dict:
        LOGGER.info(f"Reporting phishing")
        LOGGER.debug(f"Input request data: {request.get_data(as_text=True)}")
        data = json.loads(request.get_data())
        output = ReportIncidentHandler(data).handle()
        return dict(output)
