from flask import request
from flask_restful import Resource

from library.logger import LOGGER

from .handler import GetAnalysisHandler


class GetAnalysisService(Resource):
    def get(self) -> dict:
        LOGGER.info(f"Generating phishing report")
        LOGGER.debug(f"Input request data: {request.get_data(as_text=True)}")
        data = request.args.to_dict()
        output = GetAnalysisHandler(data).handle()
        return dict(output)
