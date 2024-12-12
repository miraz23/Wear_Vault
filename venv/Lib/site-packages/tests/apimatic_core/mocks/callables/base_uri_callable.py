from enum import Enum
from apimatic_core.utilities.api_helper import ApiHelper


class Environment(Enum):
    TESTING = 1


class Server(Enum):
    """An enum for API servers"""
    DEFAULT = 0
    AUTH_SERVER = 1


class BaseUriCallable:
    environments = {
        Environment.TESTING: {
            Server.DEFAULT: 'http://localhost:3000',
            Server.AUTH_SERVER: 'http://authserver:5000'
        }
    }

    def get_base_uri(self, server=Server.DEFAULT):
        """Generates the appropriate base URI for the environment and the
        server.

        Args:
            server (Configuration.Server): The server enum for which the base
            URI is required.

        Returns:
            String: The base URI.

        """
        parameters = {}

        return ApiHelper.append_url_with_template_parameters(
            self.environments[Environment.TESTING][server], parameters
        )
