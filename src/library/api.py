from collections import defaultdict
from enum import Enum
from typing import Optional, Tuple, Callable

from flask import request
from pydantic import BaseModel, ValidationError

from library.logger import LOGGER


class OutputStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class APIOutput(dict):
    def __init__(self, status: OutputStatus, message: str, data: dict):
        super().__init__(status=status.value, message=message, data=data)

    @classmethod
    def error(cls, code: str, description: str, **kwargs):
        return cls(
            status=OutputStatus.FAILURE,
            message="Request failed.",
            data={"code": code, "description": description, **kwargs},
        )

    @classmethod
    def success(cls, data: dict, message=None):
        return cls(status=OutputStatus.SUCCESS, message=message or "Ok.", data=data)


"""
Any callable that takes an object as param and returns a tuple of boolean and a string
Boolean indicates validation status and a string description is required in case validation fails.
eg:
    def validator(api_input) -> Tuple[bool, Optional[str]:
       ...
OR
    class Validator:
        def __call__(self, api_input) -> Tuple[bool, Optional[str]:
            ...
"""
InputValidator = Callable[[object], Tuple[bool, Optional[str]]]


class BaseComputer:
    def __init__(self):
        self.api_input = None

    def compute(self, api_input: BaseModel) -> APIOutput:
        """Override this method to process the input"""
        raise NotImplementedError


class APIHandler:
    def __init__(self, api_input: dict):
        self._raw_input: dict = api_input

    @property
    def computer(self) -> BaseComputer:
        """Return a child of BaseComputer"""
        raise NotImplementedError

    @property
    def api_input(self) -> BaseModel:
        """Return a subclass of BaseModel"""
        raise NotImplementedError

    @property
    def validator(self) -> Optional[InputValidator]:
        """Return a child of InputValidator"""
        raise NotImplementedError

    def handle(self) -> APIOutput:
        try:
            status, error = self._validate()
        except ValidationError as e:
            return self._handle_validation_failed_exc(e)

        if not status:
            return APIOutput.error(code="VALIDATION_FAILED", description=error)

        self._handle()

        output = self._compute()
        return output

    def _handle(self):
        """
        Override to add any additional logic here.
        This will be invoked post input validation & before computation.
        """
        pass

    def _compute(self) -> APIOutput:
        return self.computer.compute(api_input=self.api_input)

    def _validate(self) -> Tuple[bool, Optional[str]]:
        if self.validator:
            return self.validator(self.api_input)

        return True, None

    @staticmethod
    def _handle_validation_failed_exc(exc: ValidationError) -> APIOutput:
        LOGGER.exception(f"Request Validation Failed => {repr(exc)}")
        errors = defaultdict(lambda: [], {})
        for err in exc.errors():
            errors[err["type"]].append(err["loc"][0])
        return APIOutput.error(
            code="VALIDATION_FAILED",
            description="Request Body Validation Failed.",
            errors=errors,
        )


class APIGetHandler(APIHandler):
    def __init__(self, uid: str):
        self._id: str = uid
        super().__init__(request.view_args)
