""" wrapper for requests class and superwise token handling """
import requests

from superwise import logger
from superwise.config import Config
from superwise.controller.exceptions import *


def token_retry(input_func):
    """
    A decorator for token retry handling (ie, refresh token if needed)
    :param input_func:
    :return:
    """

    def wrapper(*args, **kwargs):
        res = input_func(*args, **kwargs)
        if res.status_code == 403:
            args[0].refresh_token()
            res = input_func(*args, **kwargs)
        return res

    return wrapper


class Client:
    """ Client is a wrapper for requests for superwise package """

    def __init__(self, client_id, secret, client_name, api_host, email=None, password=None):
        self.client_id = client_id
        self.secret = secret
        self.client_name = client_name
        self.api_host = api_host
        self.email = email
        self.password = password
        self.token = self.get_token()
        self.logger = logger
        self.headers = self.build_headers()

    def build_headers(self):
        """
        return the headers to send in each API call
        :return: list of headers
        """
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token,
        }

    def refresh_token(self):
        """
        refresh  bearer token

        :return: token string
        """
        return self.get_token()

    def get_token(self):
        """
        get bearer token to use in each API call

        :return: token string
        """

        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.email:
            url = "{}/identity/resources/auth/v1/user".format(Config.FRONTEGG_URL)
            params = {"email": self.email, "password": self.password}
        else:
            params = {"clientId": self.client_id, "secret": self.secret}
            url = "{}/identity/resources/auth/v1/api-token".format(Config.FRONTEGG_URL)
        res = self._post(url, params=params, headers=headers)
        error = False
        token = None
        try:
            token = res.json().get("accessToken")
        except:
            error = True

        if not token or error:
            raise SuperwiseAuthException("Error get or refresh token")
        return token

    def _post(self, url, params, headers=None):
        """
        wrapper to requests.post(), with no refresh token handling
        :param url: url string
        :param params: json paramters to send
        :param headers: headers string
        :return: Response object (requests package)
        """
        headers = self.headers if not headers else headers
        res = requests.post(url, json=params, headers=headers)
        return res

    @token_retry
    def post(self, url, params, headers=None):
        """
        wrapper for self._post() decoarted using token_retry.

        :param url: url string
        :param params: params: json paramters to send
        :param headers: headers: headers string

        :return: Response object (requests package)
        """
        return self._post(url, params, headers)

    @token_retry
    def get(self, url, query_params=None, headers=None):
        """
        wrapper for reuqests.get()

        :param url: url string
        :param query_params:  dictionary of paramters to add as query string
        :param headers: headers dictionary
        :return: Response object (requests package)
        """
        headers = self.headers if not headers else headers
        res = requests.get(url, headers=headers, params=query_params)
        return res

    @token_retry
    def delete(self, idx):
        """
        wrapper for reuqests.delete()

        :param idx: id int
        :return: Response object (requests package)
        """
        raise NotImplementedError()

    @token_retry
    def patch(self, url, params, headers=None):
        """
        wrapper for reuqests.delete()

        :return: Response object (requests package)
        """
        headers = self.headers if not headers else headers
        res = requests.patch(url, json=params, headers=headers)
        return res
