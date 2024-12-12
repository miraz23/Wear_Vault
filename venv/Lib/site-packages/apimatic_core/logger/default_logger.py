import sys

from apimatic_core_interfaces.logger.logger import Logger
import logging


class ConsoleLogger(Logger):

    def __init__(self):
        self._logger = logging.Logger(name='')
        stdout = logging.StreamHandler(stream=sys.stdout)
        fmt = logging.Formatter("%(levelname)s %(message)s")
        stdout.setFormatter(fmt)
        self._logger.addHandler(stdout)

    def log(self, level, message, params):
        """Logs a message with a specified log level and additional parameters.

        Args:
            level (int): The log level of the message.
            message (str): The message to log.
            params (dict): Additional parameters to include in the log message.
        """
        self._logger.log(level, message, *params.values())
