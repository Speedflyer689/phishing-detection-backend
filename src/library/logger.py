import logging
import sys
import traceback
import uuid


class _Logger:
    logger = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.set_request_id("AAAA")

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warn(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)

    def exception(self, message):
        """
        Use this method to log trace information of last raised exception.
        Can set up alerts on top of this method.
        """
        self.logger.error(message)
        self.logger.error(traceback.format_exc())

    def debug(self, message):
        self.logger.debug(message)

    def set_request_id(self, request_id=None):
        request_id = request_id or str(uuid.uuid4().hex)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            f"{request_id} :: %(asctime)s [%(threadName)s] [%(levelname)s]: %(message)s"
        )
        existing_handlers = self.logger.handlers
        if len(existing_handlers):
            handler = existing_handlers[0]
        else:
            handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.propagate = False


LOGGER = _Logger()
