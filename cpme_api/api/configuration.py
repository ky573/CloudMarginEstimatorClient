"""
    Cloud Prisma Margin Estimator API

    Cloud Prisma Margin Estimator (CPME) calculates margin for an uploaded portfolio according to Eurex PRISMA methodology. The application is available to both members and non-members of Eurex Clearing. It can be accessed via web user interface, see [CPME GUI](https://eurexmargins.prod.dbgservice.com), or directly through API, described here.  The key request is `/estimator`, it is the only request you need to calculate the margin. Other requests provide lists or details of instruments, available dates etc. CPME supports also greek and stress price calculation - these analytical tools are not related to the margin.  Part of the API is also Cloud Default Fund Estimator (CPDE) which *estimates* Default Fund contribution for an uploaded portfolio according to Eurex methodology. Its key resource is `/default_fund`, similar `/estimator` up to the following differences: historical calculation is not possible for Default Fund; OTC portfolio support is planned only in future.  [FAQ](https://deutsche-boerse-risk.github.io/CloudPrismaMarginEstimator/) ## API Key For API access please register at [Deutsche Boerse API website](https://console.developer.deutsche-boerse.com/apis).  There you create your project, subscribe to \"Prisma Margin Estimator\" API and get a key. Use the key in a request header as `X-DBP-APIKEY`, e.g.:  <pre> curl --header 'X-DBP-APIKEY: your-key' \\   https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-0/products </pre>  Requests from web API portals (Apiary, SwaggerHub) must contain the key as well. ## Example in Python The **[crossmargining.py](https://github.com/Deutsche-Boerse-Risk/CloudPrismaMarginEstimator-API/blob/master/examples/python/crossmargining.py)** generates a portfolio in CSV format. The portfolio consists of a 10Y EUR interest rate swap starting two days from today and a short position in Euro-Bund futures. Initial margin is calculated with and without cross margining (xm = True and xm = False, respectively) and results are printed. Replace xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx by your API key (see above).  ## Compressing request and response Both requests and responses can be compressed by gzip which can reduce response time for large requests and bypass request size limits. Use of compression in submitted request is indicated by `Content-Encoding: gzip` header. Compressed response is requested by `Accept-Encoding: gzip` header. For example:  <pre>echo '{\"portfolio_components\":[{\"type\":\"etd_portfolio\",\"etd_portfolio\":[{\"line_no\":1,\"product_id\":\"FEXD\",\"contract_date\":20301220,\"net_ls_balance\":1}]}]}' \\   | gzip \\   | curl -s -H \"X-DBP-APIKEY: your-key\" -H \"Content-Type: application/json\" \\     https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-0/estimator \\     --data-binary @- -H \"Content-Encoding: gzip\" -H \"Accept-Encoding: gzip\" \\   | gunzip </pre>  It is also possible to use compression only for request or only for response. ## Business date and time The requests can contain optional business date and time attributes. The application finds the latest snapshot from the requested business date with timestamp equal or smaller than the requested time. If time is not given then the latest timestamp of the business date is used.  It takes several minutes to start the instance for a specified snapshot, That instance can then serve subsequent requests for the same snapshot. After some inactive time the instance is shutdown. It is recommended not to specify a date and time and calculate current margin or margin as of last end-of-day, see below.  Example of requesting the latest snapshot of given date, in GET and POST type of request:  <pre>curl -H 'X-DBP-APIKEY: your-key' \\   'https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-0/series?products=FGBM&business_date=20190307' echo '{\"snapshot\":{\"business_date\":20190307},\"portfolio_components\":[{\"type\":\"etd_portfolio\",\"etd_portfolio\":[{\"line_no\":1,\"product_id\":\"FEXD\",\"contract_date\":20301220,\"net_ls_balance\":1}]}]}' \\   | curl -H 'X-DBP-APIKEY: your-key' \\     'https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-0/estimator' \\     --data-binary @- </pre>  If business date is not given, the latest business date is used. If only live=False is specified, last end-of-day is used. Calculation instance for these two requests is always up, you should not experience any delay.  Response contains identification of the selected snapshot, see attributes `business_date`, `live` and `live_timestamp`. ## Change log - 7.0.0 OTC portfolio can be submitted also as CC233 sensitivities report - 6.8.0 Security Basket ISIN, errors explained, upgrade to OpenAPI 3.0 description format - 6.5.0 ETD maturity specified preferably by contract_date - 6.3.1 Indicative margin resource - 6.2.0 Cash Market Repo, ETD CP005 and ETD CSV added to API v2 - 6.1.1 default 1T payment period for inflation swaps, ignore unknown calendars - 5.7.0 support for inflation swaps - 5.2.0 request with live=false without date means last end-of-day - 4.2.2 list of snapshots can be requested, OTC sensitivities - 4.2.1 OTC trade details resource and also included in estimator response - 4.1.1 historical snapshots also for list of products, series and currencies  # noqa: E501

    OpenAPI spec version: 2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""
import logging
import multiprocessing
import sys
import urllib3
# from six.moves import http_client as httplib
from http.client import HTTPConnection

NAME = "CPME-client"


class Configuration(object):

    def __init__(self):
        """Constructor"""
        # Default Base url
        self._url = "https://cpme.risk.dev.ams.gcp.dbgcloud.io/api/v2.0"
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
        self.logger_format = '%(asctime)-23s CPME %(levelname)-6s %(name)s %(module)-1s.%(funcName)-15s  %(message)s'
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
        # Set this to false to skip verifying SSL certificate when calling API
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
        self.connection_pool_maxsize = multiprocessing.cpu_count() * 5
        # Proxy URL
        self._proxy = None
        # Safe chars for path_param
        self._enable_pooling = None
        self._pool_size = 4
        self._max_size = None
        self._verbose = None
        self._timeout = None
        self._env = "PROD"
        self._request_timeout = None
        self._return_json = None

    @property
    def return_json(self):
        return self._return_json

    @return_json.setter
    def return_json(self, value: bool):
        self._return_json = value

    @property
    def enable_logging(self):
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
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @property
    def request_timeout(self):
        return self._request_timeout

    @request_timeout.setter
    def request_timeout(self, value):
        self._request_timeout = value

    @property
    def pool_size(self):
        return self._pool_size

    @pool_size.setter
    def pool_size(self, value):
        self._pool_size = value

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, value):
        self._max_size = value

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
        return self._verbose

    @verbose.setter
    def verbose(self, value):
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
    def logger_format(self, value):
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
    def logger_file(self, value):
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
        """Debug status

        :param value: The debug status, True or False.
        :type: bool
        """
        return self._debug

    @debug.setter
    def debug(self, value):
        """Debug status

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
    def logger_format(self, value):
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
        """Gets Auth Settings dict for api client.

        :return: The Auth Settings information dict.
        """
        return {
        }

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
