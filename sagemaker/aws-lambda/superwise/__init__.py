""" root for supwrwise pacakge, set logger and load config"""
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.ERROR)

from superwise.config import Config
from superwise.controller.client import Client
from superwise.controller.data import DataController


class Superwise:
    """ Superwise class - main class for superwise package """

    def __init__(
        self,
        client_id=None,
        secret=None,
        client_name=None,
        _rest_client=None,
        email=None,
        password=None,
        _fegg_url=None,
        _superwise_host=None,
    ):
        """
        constructer for Superwise class

        :param client_id:
        :param secret:
        :param client_name:
        :param _rest_client: inject rest client if needed (allow mocking of rest api calls)
        """
        self.logger = logger
        if _superwise_host:
            Config.SUPERWISE_HOST = _superwise_host
        if _fegg_url:
            Config.FRONTEGG_URL = _fegg_url
        client_id = client_id or os.environ.get("SUPERWISE_CLIENT_ID")
        secret = secret or os.environ.get("SUPERWISE_SECRET")
        client_name = client_name or os.environ.get("SUPERWISE_CLIENT_NAME")
        if email and password:
            self.logger.info("login using user and password")
        elif client_id is None or secret is None or client_name is None:
            raise Exception("client_id, secret, client_name are mendatory fields ")
        api_host = Config.SUPERWISE_HOST
        if not _rest_client:
            _rest_client = Client(client_id, secret, client_name, api_host, email, password)
        self.data = DataController(_rest_client, self)
