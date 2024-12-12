import logging

from apimatic_core_interfaces.logger.logger import Logger


class ApiLogger(Logger):

    def __init__(self):
        self._logger = logging.getLogger('mocked_logger')

    def log(self, level, message, params):
        self._logger.log(level, message, *params.values())


