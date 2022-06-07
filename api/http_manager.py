import json
from typing import Optional, Dict, Any, Union

from requests import Request

APP_JSON = ACCEPT = 'application/json'
APP_X_WWW_FORM_URLENCODED = 'application/x-www-form-urlencoded'
TEXT_PLAIN = 'text/plain'


class HttpManager:

    """
    Class that wraps requests.Request object with needed arguments
    """
    @staticmethod
    def __json_dumps(obj: object) -> str:
        """
        Serialize ``obj`` to a JSON formatted ``str``
        :param obj: object to serialize
        """
        if isinstance(obj, str):
            return obj
        return json.dumps(obj)

    @classmethod
    def __json_headers(cls, passed_headers: Optional[Dict[Any, Any]]) -> Dict[Any, Any]:
        """
        Update default json headers with passed headers, if any
        :param passed_headers: headers dictionary to update
        """
        headers = {'Content-Type': APP_JSON, 'Accept': ACCEPT}
        if passed_headers:
            headers.update(passed_headers)
        return headers

    @classmethod
    def get(cls, url: str, params: Optional[Dict[Any, Any]] = None, **kwargs: Dict[Any, Any]) -> Request:
        """
        Request object wrapper with GET method
        :param url: url to perform request
        :param params: URL parameters to append to the URL
        """
        return Request(method='GET', url=url, params=params, **kwargs)

    @classmethod
    def post(cls, url: str, data: Union[Dict[Any, Any], str, None] = None, **kwargs: Dict[Any, Any]) -> Request:
        """
        Request object wrapper with POST method
        :param url: url to perform request
        :param data: the body to attach to the request. If a dictionary is provided, form-encoding will take place.
        """
        return Request(method='POST', url=url, data=data, **kwargs)

    @classmethod
    def post_json(cls, url: str, data: Dict[Any, Any],
                  headers: Optional[Dict[Any, Any]] = None,
                  **kwargs: Dict[Any, Any]) -> Request:
        """
        The same as post method but with application/json headers and serialized data
        :param url: url to perform request
        :param data: the body to attach to the request. If a dictionary is provided, form-encoding will take place.
        :param headers: request headers
        """
        return cls.post(url, data=cls.__json_dumps(data), headers=cls.__json_headers(headers), **kwargs)

    @classmethod
    def delete(cls, url: str,
               params: Optional[Dict[Any, Any]] = None,
               **kwargs: Any) -> Request:
        """
        Request object wrapper with DELETE method
        :param url: url to perform request
        :param params: URL parameters to append to the URL
        """
        return Request(method='DELETE', url=url, params=params, **kwargs)

    @classmethod
    def delete_json(cls, url: str, data: Dict[Any, Any],
                    headers: Optional[Dict[Any, Any]] = None,
                    **kwargs: Dict[Any, Any]) -> Request:
        """
        The same as delete method but with application/json headers and serialized data
        :param url: url to perform request
        :param data: the body to attach to the request. If a dictionary is provided, form-encoding will take place.
        :param headers: request headers
        """
        return cls.delete(url, data=cls.__json_dumps(data), headers=cls.__json_headers(headers), **kwargs)

    @classmethod
    def put(cls, url: str, data: Union[Dict[Any, Any], str, None] = None, **kwargs: Dict[Any, Any]) -> Request:
        """
        Request object wrapper with PUT method
        :param url: url to perform request
        :param data: the body to attach to the request. If a dictionary is provided, form-encoding will take place.
        """
        return Request(method='PUT', url=url, data=data, **kwargs)

    @classmethod
    def put_json(cls, url: str, data: Dict[Any, Any],
                 headers: Optional[Dict[Any, Any]] = None,
                 **kwargs: Dict[Any, Any]) -> Request:
        """
        The same as put method but with application/json headers and serialized data
        :param url: url to perform request
        :param data: the body to attach to the request. If a dictionary is provided, form-encoding will take place.
        :param headers: request headers
        """
        return cls.put(url, data=cls.__json_dumps(data), headers=cls.__json_headers(headers), **kwargs)

    @classmethod
    def patch(cls, url: str, data: Union[Dict[Any, Any], str, None] = None, **kwargs: Dict[Any, Any]) -> Request:
        """
        Request object wrapper with PATCH method
        :param url: url to perform request
        :param data: the body to attach to the request. If a dictionary is provided, form-encoding will take place.
        """
        return Request(method='PATCH', url=url, data=data, **kwargs)

    @classmethod
    def patch_json(cls, url: str, data: Dict[Any, Any],
                   headers: Optional[Dict[Any, Any]] = None,
                   **kwargs: Dict[Any, Any]) -> Request:
        """
        The same as patch method but with application/json headers and serialized data
        :param url: url to perform request
        :param data: the body to attach to the request. If a dictionary is provided, form-encoding will take place.
        :param headers: request headers
        """
        return cls.patch(url, data=cls.__json_dumps(data), headers=cls.__json_headers(headers), **kwargs)
