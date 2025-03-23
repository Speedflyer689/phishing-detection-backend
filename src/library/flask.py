import json
from collections import defaultdict

from flask import request, Response

from pydantic import ValidationError

from .api import APIOutput
from .logger import LOGGER
from .exceptions import CustomException, MLModelException

def handle_pydantic_validation_errors(exc: ValidationError) -> APIOutput:
    LOGGER.exception(f"Request Validation Failed => {repr(exc)}")
    errors = defaultdict(lambda: [], {})
    for err in exc.errors():
        errors[err["type"]].append(err["loc"][0])
    return APIOutput.error(
        code="VALIDATION_FAILED",
        description="Request Body Validation Failed.",
        errors=errors,
    )


def handle_400(exc) -> APIOutput:
    if isinstance(exc, CustomException):
        LOGGER.exception(f"Error computing => {repr(exc)}")
        return APIOutput.error(code="CLIENT_ERROR", description=f"{exc.description}")

    if isinstance(exc, MLModelException):
        LOGGER.exception(f"Error computing => {repr(exc)}")
        return APIOutput.error(code="ML_ERROR", description=f"{exc.description}")

    raise exc


def handle_generic_exception(exc: Exception) -> APIOutput:
    LOGGER.exception(f"Error computing => {repr(exc)}")
    return APIOutput.error(code="INTERNAL_SERVER_ERROR", description="Internal Server Error.")


def before_request():
    tag = "Before Request Middleware"
    LOGGER.set_request_id()
    LOGGER.info(f"{tag} => invoked {request.url}")
    LOGGER.info(f"{tag} => headers received => {dict(request.headers)}")
    LOGGER.info(f"{tag} => payload received => {request.get_data()}")


def after_request(response):
    tag = "After Request Middleware"
    LOGGER.info(f"{tag} invoked...")
    return get_output(response)


def get_output(response):
    try:
        response_text = json.loads(response.response[0])
        headers = response.headers

        if response_text.get("status") == "SUCCESS":
            return Response(response=json.dumps(response_text), status=200, headers=headers)
        elif response_text.get("status") == "FAILURE":
            return Response(response=json.dumps(response_text), status=400, headers=headers)
        elif response_text.get("status") == "INTERNAL_SERVER_ERROR":
            return Response(response=json.dumps(response_text), status=500, headers=headers)
    except Exception as e:
        LOGGER.exception(f"Exception while processing response => {repr(e)}")
        return response

    return response
