"""
"""
import logging
import multiprocessing
import sys
import urllib3
from http.client import HTTPConnection

NAME = "CPME-client"


class Configuration(object):
    """
    Configuration class
    """

    def __init__(self):
        """Constructor"""
        # Default Base url
        # self._url = "https://eurexmargins.prod.dbgservice.com/api/v2.0"
        self._url = "https://api.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-2-0-0"
        # self._url = "https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-0"
        # Temp file folder for downloading files
        self.temp_folder_path = None
        # Authentication Settings
        # dict to store API key(s)
        self._api_key = {}
        # Username for HTTP basic authentication
        self._username = ""
        # Password for HTTP basic authentication
        self._password = ""
        # Logging Settings
        self.loggers = {"package_logger": logging.getLogger("cpme_api"),
                        "urllib3_logger": logging.getLogger("urllib3")}
        # Log format
        self.logger_format = '%(asctime)-23s api-client %(levelname)-6s %(name)s %(module)-1s.%(funcName)-15s  %(message)s'
        # Log stream handler
        self.logger_stream_handler = None
        # Log file handler
        self.logger_file_handler = None
        # Debug file location
        self._logger_file = None
        self._enable_logging = False
        # Debug switch
        self._debug = False
        # SSL/TLS verification
        # Set this to False to skip verifying SSL certificate when calling API
        # from https server.
        self._verify_ssl = False
        # Set this to customize the certificate file to verify the peer.
        self._ssl_ca_cert = None
        # client certificate file
        self._cert_file = None
        # client key file
        self._key_file = None
        # Set this to True/False to enable/disable SSL hostname verification.
        self.assert_hostname = None
        # urllib3 connection pool's maximum number of connections saved
        # per pool. urllib3 uses 1 connection as default value, but this is
        # not the best value when you are making a lot of possibly parallel
        # requests to the same host, which is often the case here.
        # cpu_count * 5 is used as default value to increase performance.
        self._connection_pool_maxsize = multiprocessing.cpu_count() * 5
        # Proxy URL
        self._proxy = None
        # Safe chars for path_param
        self._enable_pooling = None
        self._verbose = None
        self._timeout = None
        self._env = "PROD"
        self._request_timeout = None
        self._return_json = True

    @property
    def return_json(self):
        return self._return_json

    @return_json.setter
    def return_json(self, value: bool):
        self._return_json = value

    @property
    def enable_logging(self):
        """Enable logging for client loggers. It is disabled as default.

        While enable the stdout logging with default INFO severity is established. The user can define logger_file attribute to enable file logger.

        :param value:
        :type: bool
        """
        return self._enable_logging

    @enable_logging.setter
    def enable_logging(self, value: bool):
        self._enable_logging = value
        if value:
            if not self.logger_stream_handler:
                self.logger_stream_handler = logging.StreamHandler(sys.stdout)
            self.logger_stream_handler.setFormatter(logging.Formatter(self.logger_format))
            for logger in self.loggers.values():
                logger.addHandler(self.logger_stream_handler)
                if self.debug:
                    logger.setLevel(logging.DEBUG)
                else:
                    logger.setLevel(logging.INFO)
            self.loggers['package_logger'].info(f'Logger start.')
        else:
            for logger in self.loggers.values():
                logger.warning('Logger is disabled!')
                if self.logger_stream_handler:
                    logger.removeHandler(self.logger_stream_handler)

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, value):
        self._env = value

    @property
    def key_file(self):
        return self._key_file

    @key_file.setter
    def key_file(self, value):
        self._key_file = value

    @property
    def cert_file(self):
        return self._cert_file

    @cert_file.setter
    def cert_file(self, value):
        self._cert_file = value

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        self._proxy = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @property
    def api_key(self):
        """
        User unique key .....

        :param value:
        :type: str:
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        """
        User unique key .....

        :param value:
        :type: str:
        """
        self._api_key = value

    @property
    def request_timeout(self):
        """Maximum timeout of individual request in seconds.

        :param value:
        :type: int
        """
        return self._request_timeout

    @request_timeout.setter
    def request_timeout(self, value):
        """Maximum timeout of individual request in seconds.

        :param value:
        :type: int
        """
        self._request_timeout = value

    @property
    def connection_pool_maxsize(self):
        """Number of pools of urrllib connector

        :param value:
        :type: int
        """
        return self._connection_pool_maxsize

    @connection_pool_maxsize.setter
    def connection_pool_maxsize(self, value: int):
        """Number of pools of urrllib connector

        :param value:
        :type: int
        """
        self._connection_pool_maxsize = value

    @property
    def verify_ssl(self):
        return self._verify_ssl

    @verify_ssl.setter
    def verify_ssl(self, value):
        self._verify_ssl = value

    @property
    def enable_pooling(self):
        return self._enable_pooling

    @enable_pooling.setter
    def enable_pooling(self, value):
        self._enable_pooling = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def ssl_ca_cert(self):
        return self._ssl_ca_cert

    @ssl_ca_cert.setter
    def ssl_ca_cert(self, value):
        self._ssl_ca_cert = value

    @property
    def verbose(self):
        """Enable/Disable additional info messages into the logger

        :param value:
        :type: bool
        """
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool):
        """Enable/Disable additional info messages into the logger

        :param value:
        :type: bool
        """
        self._verbose = value

    @property
    def logger_format(self):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        return self._logger_format

    @logger_format.setter
    def logger_format(self, value: str):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        self._logger_format = value
        self.logger_formatter = logging.Formatter(self._logger_format)

    @property
    def logger_file(self):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        return self._logger_file

    @logger_file.setter
    def logger_file(self, value: str):
        """The logger file.

        If the logger_file is None, then add stream handler and remove file
        handler. Otherwise, add file handler and remove stream handler.

        :param value: The logger_file path.
        :type: str
        """
        self._logger_file = value
        if self._logger_file:
            self.logger_file_handler = logging.FileHandler(self._logger_file)
            self.logger_file_handler.setFormatter(logging.Formatter(self.logger_format))
            for logger in self.loggers.values():
                logger.addHandler(self.logger_file_handler)
                if self.debug:
                    logger.setLevel(logging.DEBUG)
                else:
                    logger.setLevel(logging.INFO)
            self.loggers['package_logger'].info(f'Logging to file {self.logger_file_handler.baseFilename}')

    @property
    def debug(self):
        """
        Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        return self._debug

    @debug.setter
    def debug(self, value: bool):
        """
        Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        self._debug = value
        if self._debug:
            # if debug status is True, turn on debug logging
            for _, logger in self.loggers.items():
                logger.setLevel(logging.DEBUG)
            # turn on httplib debug
            HTTPConnection.debuglevel = 1
            self.info()
        else:
            # if debug status is False, turn off debug logging,
            # setting log level to default `logging.WARNING`
            for _, logger in self.loggers.items():
                logger.setLevel(logging.INFO)
            # turn off httplib debug
            HTTPConnection.debuglevel = 0

    @property
    def logger_format(self):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        return self._logger_format

    @logger_format.setter
    def logger_format(self, value: str):
        """The logger format.

        The logger_formatter will be updated when sets logger_format.

        :param value: The format string.
        :type: str
        """
        self._logger_format = value
        self.logger_formatter = logging.Formatter(self._logger_format)

    def get_basic_auth_token(self):
        """Gets HTTP basic authentication header (string).

        :return: The token for basic HTTP authentication.
        """
        return urllib3.util.make_headers(
            basic_auth=self.username + ':' + self.password
        ).get('authorization')

    def auth_settings(self):
        return {}

    def info(self):
        self.loggers['package_logger'].debug(str({k.lstrip('_'): v for k, v in self.__dict__.items()}))

    def to_debug_report(self):
        """Gets the essential information for debugging.

        :return: The report for debugging.
        """
        return "Python SDK Debug Report:\n"\
               "OS: {env}\n"\
               "Python Version: {pyversion}\n"\
               "Version of the API: 2.0\n"\
               "SDK Package Version: 1.0.0".\
               format(env=sys.platform, pyversion=sys.version)
