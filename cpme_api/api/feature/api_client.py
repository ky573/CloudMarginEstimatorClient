# import multiprocessing.dummy as multiprocessing
#from multiprocessing.pool import ThreadPool
from multiprocessing.dummy import Pool as ThreadPool

import ipdb

from cpme_api.api.feature import rest
from requests.models import Response
from cpme_api.api.configuration import Configuration


HEADER = {'Content-Type': 'application/json'}
USER_AGENT = {'User-Agent': 'CometApi/3.0.0/python'}


class ApiClient(object):
    """Generic API client for Swagger client library builds.

    Swagger generic API client. This client handles the client-
    server communication, and is invariant across implementations.

    :param pooling: Flag enable or disable PoolingManager of Urllib
        if false then simple request() from requests libt will be called
    :return response: if pooling=False returns requests.models.Response
            else returns dict
    """

    def __init__(self, configuration: Configuration):
        if configuration is None:
            configuration = Configuration()
        self.config = configuration
        self.rest_client = rest.RESTClientObject(configuration)
        self.pooling = configuration.enable_pooling
        self.default_headers = {}
        self.client_side_validation = False  # configuration.client_side_validation
        self.pool = ThreadPool()

    def close(self):
        self.pool.close()
        self.pool.join()

    @staticmethod
    def _split_parameters(params: dict, api_key: dict = None) -> (dict, dict):
        n_params = {k: params[k] for k in params if k in params.get('defined')}
        if api_key:
            HEADER.update({'x_dbp_apikey': params.get('api_key', api_key)})
            if 'x_dbp_apikey' in params:
                n_params.pop('x_dbp_apikey')
        elif 'x_dbp_apikey' in params:
            HEADER.update({'x_dbp_apikey': params['x_dbp_apikey']})
            n_params.pop('x_dbp_apikey')
        elif 'api_key' in params:
            HEADER.update({'x_dbp_apikey': params['api_key']})
        HEADER.update(USER_AGENT)
        if 'q_path' in params:
            return HEADER, n_params, params.pop('q_path')
        else:
            return HEADER, n_params, None

    @property
    def user_agent(self):
        """User agent for this API client"""
        return self.default_headers['User-Agent']

    @user_agent.setter
    def user_agent(self, value):
        self.default_headers['User-Agent'] = value

    def set_default_header(self, header_name, header_value):
        self.default_headers[header_name] = header_value

    def call_api(self, endpoint, method, params={}, response_type=None,
                 body=None, request_timeout=None,
                 serialization=None, collection_format={}):
        """Makes the HTTP request (synchronous) and returns deserialized data.

        To make an async request, set the async_req parameter.

        :param endpoint: Path to method endpoint.
        :param method: Method to call.
        :param params: Path or Query  parameters in the url.
        :param body: Request body.
        :param response_type: Response data type.
        :param async_req bool: execute request asynchronously if True
        :param serialization bool: if False or None the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. if True return Data Classed object tree.
        :param request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param collection_formats: dict of collection formats for path, query,
            header, and post parameters.
        :return:
            If async_req parameter is True,
            the request will be called asynchronously.
            The method will return the request thread.
            If parameter async_req is False or missing,
            then the method will return the response directly.
        """
        if not params.get('async_req'):
            return self._call_api(endpoint, method, params,
                                  body, serialization,
                                  request_timeout, response_type, collection_format)
        else:
            thread = self.pool.apply_async(self._call_api, (endpoint,
                                           method, params, body,
                                           request_timeout, request_timeout, response_type, collection_format))
        return thread

    def parameters_to_tuples(self, params, collection_formats):
        """Get parameters as list of tuples, formatting collections.

        :param params: Parameters as dict or list of two-tuples
        :param dict collection_formats: Parameter collection formats
        :return: Parameters as list of tuples, collections formatted
        """
        new_params = []
        if collection_formats is None:
            collection_formats = {}
        for k, v in params.items():  # noqa: E501
            if k in collection_formats:
                collection_format = collection_formats[k]
                if collection_format == 'multi':
                    new_params.extend((k, value) for value in v)
                else:
                    if collection_format == 'ssv':
                        delimiter = ' '
                    elif collection_format == 'tsv':
                        delimiter = '\t'
                    elif collection_format == 'pipes':
                        delimiter = '|'
                    else:  # csv is the default
                        delimiter = ','
                    new_params.append(
                        (k, delimiter.join(str(value) for value in v)))
            else:
                new_params.append((k, v))
        return new_params

    def _call_api(self, endpoint, method, params={}, body=None,
                  request_timeout=None, serialization=None, response_type=None, collection_format=None):

        header_params, query_params, path_params = self._split_parameters(params, self.config.api_key)
        query_params = self.parameters_to_tuples(query_params, collection_format)

        if params.get('env') is None:
            if self.config.env:
                environment = self.config.env

        if request_timeout is None:
            # load from parameters
            if params.get('timeout') is None:
                request_timeout = self.config.request_timeout
            else:
                request_timeout = params['timeout']

        # request url
        if path_params:
            url = self.config.url + endpoint + path_params
        else:
            url = self.config.url + endpoint

        # perform request and return response
        response_data = self.request(
            method, url, endpoint, query_params=query_params, headers=header_params,
            body=body, request_timeout=request_timeout, verbose=params.get('verbose', True))

        if serialization:
            return self.deserialize(response_data, response_type)

        if isinstance(response_data, Response):
            # Response from requests lib
            return response_data
        else:
            # Response of poolmanager urllib
            if self.config.return_json:
                return response_data.json
            else:
                return response_data

    def request(self, method, url, endpoint, query_params=None, headers=None,
                body=None, request_timeout=None,
                verbose=False, preload_content=True, post_params=None):
        """Makes the HTTP request using RESTClient."""
        if method == "GET":
            return self.rest_client.GET(url,
                                        endpoint,
                                        query_params=query_params,
                                        _preload_content=preload_content,
                                        _request_timeout=request_timeout,
                                        headers=headers,
                                        verbose=verbose)
        elif method == "HEAD":
            return self.rest_client.HEAD(url,
                                         query_params=query_params,
                                         _preload_content=preload_content,
                                         _request_timeout=request_timeout,
                                         headers=headers,
                                         verbose=verbose)
        elif method == "OPTIONS":
            return self.rest_client.OPTIONS(url,
                                            query_params=query_params,
                                            headers=headers,
                                            post_params=post_params,
                                            _preload_content=preload_content,
                                            _request_timeout=request_timeout,
                                            body=body,
                                            verbose=verbose)
        elif method == "POST":
            return self.rest_client.POST(url,
                                         endpoint,
                                         query_params=query_params,
                                         headers=headers,
                                         post_params=post_params,
                                         _preload_content=preload_content,
                                         _request_timeout=request_timeout,
                                         body=body,
                                         verbose=verbose)
        elif method == "PUT":
            return self.rest_client.PUT(url,
                                        query_params=query_params,
                                        headers=headers,
                                        post_params=post_params,
                                        _preload_content=preload_content,
                                        _request_timeout=request_timeout,
                                        body=body,
                                        verbose=verbose)
        elif method == "PATCH":
            return self.rest_client.PATCH(url,
                                          query_params=query_params,
                                          headers=headers,
                                          post_params=post_params,
                                          _preload_content=preload_content,
                                          _request_timeout=request_timeout,
                                          body=body,
                                          verbose=verbose)
        elif method == "DELETE":
            return self.rest_client.DELETE(url,
                                           query_params=query_params,
                                           headers=headers,
                                           _preload_content=preload_content,
                                           _request_timeout=request_timeout,
                                           body=body,
                                           verbose=verbose)
        else:
            raise ValueError(
                "http method must be `GET`, `HEAD`, `OPTIONS`,"
                " `POST`, `PATCH`, `PUT` or `DELETE`."
            )
