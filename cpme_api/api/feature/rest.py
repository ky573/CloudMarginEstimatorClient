from __future__ import absolute_import

import io
import json
import re
import ssl
import certifi
from urllib.parse import urlencode

import ipdb

try:
    import urllib3
except ImportError:
    raise ImportError('Swagger python client requires urllib3.')

from cpme_api.api.configuration import Configuration
import requests
from requests.models import Response


urllib3.disable_warnings()


class RESTResponse(io.IOBase):
    def __init__(self, resp):
        if isinstance(resp, Response):
            self.requests_response = resp
            self.status = resp.status_code
            self.reason = resp.reason
            self.headers = resp.headers
            self.data = resp.content
        else:
            self.urllib3_response = resp
            self.status = resp.status
            self.reason = resp.reason
            self.headers = resp.getheaders()
            # In the python 3, the response.data is bytes.
            # we need to decode it to string.
            self.data = resp.data.decode('utf8')

        if self.status != 200:
            self.json = {}
        else:
            self.json = resp.json()

    def getheader(self, name, default=None):
        """Returns a given response header."""
        return self.headers.get(name, default)


def shorten_body(body: dict) -> str:
    str_body = str(body)
    if (size := len(str_body)) > 300:
        str_body = '[' + str(size) + 'bytes]' + str_body[0:150] + '...' + str_body[-150:]
    return str_body


class RESTClientObject(object):

    def __init__(self, configuration: Configuration, pools_size=4, maxsize=None):
        self.pooling = configuration.enable_pooling
        self.log = configuration.loggers.get('package_logger')
        # urllib3.PoolManager will pass all kw parameters to connectionpool
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/poolmanager.py#L75  # noqa: E501
        # https://github.com/shazow/urllib3/blob/f9409436f83aeb79fbaf090181cd81b784f1b8ce/urllib3/connectionpool.py#L680  # noqa: E501
        # maxsize is the number of requests to host that are allowed in parallel  # noqa: E501
        # Custom SSL certificates and client certificates: http://urllib3.readthedocs.io/en/latest/advanced-usage.html  # noqa: E501

        # cert_reqs
        if configuration.verify_ssl:
            cert_reqs = ssl.CERT_REQUIRED
        else:
            cert_reqs = ssl.CERT_NONE

        # ca_certs
        if configuration.ssl_ca_cert:
            ca_certs = configuration.ssl_ca_cert
        else:
            # if not set certificate file, use Mozilla's root certificates.
            ca_certs = certifi.where()

        addition_pool_args = {}

        if maxsize is None:
            if configuration.connection_pool_maxsize is not None:
                maxsize = configuration.connection_pool_maxsize
            else:
                maxsize = 4

        # https pool manager
        if configuration.proxy:
            self.pool_manager = urllib3.ProxyManager(
                num_pools=pools_size,
                maxsize=maxsize,
                cert_reqs=cert_reqs,
                ca_certs=ca_certs,
                cert_file=configuration.cert_file,
                key_file=configuration.key_file,
                proxy_url=configuration.proxy,
                **addition_pool_args
            )
        else:
            self.pool_manager = urllib3.PoolManager(
                num_pools=pools_size,
                maxsize=maxsize,
                cert_reqs=cert_reqs,
                ca_certs=ca_certs,
                cert_file=configuration.cert_file,
                key_file=configuration.key_file,
                **addition_pool_args
            )
        if not self.pooling:
            self.pool_manager = None

    def request(self, method, url, query_params=None, headers=None,
                body=None, post_params=None, _preload_content=True,
                _request_timeout=None):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param query_params: query parameters in the url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        method = method.upper()
        assert method in ['GET', 'HEAD', 'DELETE', 'POST', 'PUT',
                          'PATCH', 'OPTIONS']

        if post_params and body:
            raise ValueError(
                "body parameter cannot be used with post_params parameter."
            )

        post_params = post_params or {}
        headers = headers or {}

        timeout = None
        if _request_timeout:
            if isinstance(_request_timeout, (int, )):
                timeout = urllib3.Timeout(total=_request_timeout)
            elif (isinstance(_request_timeout, tuple) and
                  len(_request_timeout) == 2):
                timeout = urllib3.Timeout(
                    connect=_request_timeout[0], read=_request_timeout[1])

        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        try:
            # For `POST`, `PUT`, `PATCH`, `OPTIONS`, `DELETE`
            if method in ['POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE']:
                if query_params:
                    url += '?' + urlencode(query_params)
                if re.search('json', headers['Content-Type'], re.IGNORECASE):
                    request_body = '{}'
                    if body is not None:
                        request_body = json.dumps(body)
                    resp = self.pool_manager.request(
                        method, url,
                        body=request_body,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                elif headers['Content-Type'] == 'application/x-www-form-urlencoded':  # noqa: E501
                    resp = self.pool_manager.request(
                        method, url,
                        fields=post_params,
                        encode_multipart=False,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                elif headers['Content-Type'] == 'multipart/form-data':
                    # must del headers['Content-Type'], or the correct
                    # Content-Type which generated by urllib3 will be
                    # overwritten.
                    del headers['Content-Type']
                    resp = self.pool_manager.request(
                        method, url,
                        fields=post_params,
                        encode_multipart=True,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                # Pass a `string` parameter directly in the body to support
                # other content types than Json when `body` argument is
                # provided in serialized form
                elif isinstance(body, str):
                    request_body = body
                    resp = self.pool_manager.request(
                        method, url,
                        body=request_body,
                        preload_content=_preload_content,
                        timeout=timeout,
                        headers=headers)
                else:
                    # Cannot generate the request from given parameters
                    msg = """Cannot prepare a request message for provided
                             arguments. Please check that your arguments match
                             declared content type."""
                    raise ApiException(status=0, reason=msg)
            # For `GET`, `HEAD`
            else:
                resp = self.pool_manager.request(method, url,
                                                 fields=query_params,
                                                 preload_content=_preload_content,
                                                 timeout=timeout,
                                                 headers=headers)
        except urllib3.exceptions.SSLError as e:
            msg = "{0}\n{1}".format(type(e).__name__, str(e))
            raise ApiException(status=0, reason=msg)

        if _preload_content:
            resp = RESTResponse(resp)
            # log response body
            self.log.debug(f"{method} url: {url} headers: {resp.headers} response_body: {resp.data}")

        if not 200 <= resp.status <= 299:
            raise ApiException(http_resp=resp)

        return resp

    def GET(self, url, endpoint, headers=None, query_params=None, _preload_content=True,
            _request_timeout=None, verbose=True):
        if verbose:
            msg_timeout = ''

            if _request_timeout:
                msg_timeout = f'Timeout = {_request_timeout}'

            self.log.info(f"{endpoint}\tHEADER:{headers} PARAMS:{query_params} URL:{url} {msg_timeout}")
        if self.pooling:
            return self.request("GET", url,
                                headers=headers,
                                _preload_content=_preload_content,
                                _request_timeout=_request_timeout,
                                query_params=query_params)
        else:
            # temporarily for requests lib
            resp = requests.get(url,
                                params=query_params,
                                headers=headers,
                                verify=False,
                                timeout=_request_timeout,
                                stream=True)
            if _preload_content:
                resp = RESTResponse(resp)
                # log response body
                self.log.debug(f"GET url: {url} headers: {resp.headers} response_body: {resp.data}")

            if not 200 <= resp.status <= 299:
                raise ApiException(http_resp=resp)

            return resp

    def HEAD(self, url, headers=None, query_params=None, _preload_content=True,
             _request_timeout=None):
        return self.request("HEAD", url,
                            headers=headers,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            query_params=query_params)

    def OPTIONS(self, url, headers=None, query_params=None, post_params=None,
                body=None, _preload_content=True, _request_timeout=None):
        return self.request("OPTIONS", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def DELETE(self, url, headers=None, query_params=None, body=None,
               _preload_content=True, _request_timeout=None):
        return self.request("DELETE", url,
                            headers=headers,
                            query_params=query_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def POST(self, url, endpoint, headers=None, query_params=None, post_params=None,
             body=None, _preload_content=True, _request_timeout=None, verbose=True):
        if verbose:
            msg_timeout = ''

            if _request_timeout:
                msg_timeout = f'Timeout = {_request_timeout}'

            self.log.info(f"{endpoint}\tHEADER:{headers} PARAMS:{query_params} URL:{url} {msg_timeout}")

        if self.pooling:
            return self.request("POST", url,
                                headers=headers,
                                query_params=query_params,
                                post_params=post_params,
                                _preload_content=_preload_content,
                                _request_timeout=_request_timeout,
                                body=body)
        else:
            return requests.post(url,
                                 headers=headers,
                                 verify=False,
                                 timeout=_request_timeout,
                                 stream=False,
                                 json=body)

    def PUT(self, url, headers=None, query_params=None, post_params=None,
            body=None, _preload_content=True, _request_timeout=None):
        return self.request("PUT", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)

    def PATCH(self, url, headers=None, query_params=None, post_params=None,
              body=None, _preload_content=True, _request_timeout=None):
        return self.request("PATCH", url,
                            headers=headers,
                            query_params=query_params,
                            post_params=post_params,
                            _preload_content=_preload_content,
                            _request_timeout=_request_timeout,
                            body=body)


class ApiException(Exception):

    def __init__(self, status=None, reason=None, http_resp=None):
        if http_resp:
            self.status = http_resp.status
            self.reason = http_resp.reason
            self.body = http_resp.data
            self.headers = http_resp.headers
        else:
            self.status = status
            self.reason = reason
            self.body = None
            self.headers = None

    def __str__(self):
        """Custom error messages for exception"""
        error_message = "({0})\n"\
                        "Reason: {1}\n".format(self.status, self.reason)
        if self.headers:
            error_message += "HTTP response headers: {0}\n".format(
                self.headers)

        if self.body:
            error_message += "HTTP response body: {0}\n".format(self.body)

        return error_message
