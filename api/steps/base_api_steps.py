import logging
from urllib.parse import urlparse

import requests


class UnexpectedStatusCode(requests.RequestException):
    def __init__(self, message, response_content):
        self.response_content = response_content
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}. Response content: {self.response_content}'


class BaseApiSteps:
    """
    Class for usage in API's testing, handles session, requests calling
    """
    def __init__(self, base_url,
                 session=None,
                 timeout=None,
                 return_json=True,
                 ):
        """
        :param base_url: base url that will be prepended to request url/path (e.g. 'http://host:port/api')
        :param session: session objects
        :param timeout: time to wait response
        :param return_json: flag to return json or just response object
        """
        self._base_url = base_url
        self._session = session or requests.Session()
        self._timeout = timeout
        self._return_json = return_json

    @staticmethod
    def _has_scheme(url: str) -> bool:
        """
        Check if provided url has scheme
        """
        parsed_url = urlparse(url)
        return bool(parsed_url.scheme)

    @property
    def session(self) -> requests.Session:
        """
        Session property
        """
        return self._session

    def call_with_log(self, req, *args, **kwargs):
        """
        Make request with logging
        """
        logging.debug('Request body: %s', req.data)
        resp = self.call(req, *args, **kwargs)
        logging.debug('Response: %s', resp)
        return resp

    def call(self,
             request,
             timeout=None,
             expected_status_code=None,
             return_json=None,
             allow_redirects=True,
             ):
        """
        Send request wrapper
        :param request: request to send
        :param timeout: time to wait response
        :param expected_status_code: status code we'd expect
        :param return_json: flag to return json or response object
        :param allow_redirects: flag to allow redirects or not
        """
        if timeout is None:
            timeout = self._timeout
        if return_json is None:
            return_json = self._return_json

        if self._has_scheme(request.url):
            raise ValueError('request.url must be relative, but got: {url}'.format(url=request.url))
        request.url = self._base_url + request.url

        session = self.session or requests.Session()
        prepared_request = session.prepare_request(request)

        response = session.send(prepared_request, timeout=timeout, allow_redirects=allow_redirects)
        logging.debug(f'Response headers: {response.headers}')

        if expected_status_code:
            actual_status_code = response.status_code
            if isinstance(expected_status_code, int):
                expected_status_code = [expected_status_code]
            if actual_status_code not in expected_status_code:
                err_msg = 'Expected status codes are {expected}, but was {actual}'.format(
                    expected=expected_status_code, actual=actual_status_code)
                raise UnexpectedStatusCode(err_msg, response_content=response.content.decode())

        if return_json:
            return response.json()
        else:
            return response
