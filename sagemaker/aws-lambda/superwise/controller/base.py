""" Base controller class for superwise package """
import json
import traceback
from abc import ABC
from abc import ABCMeta
from abc import abstractproperty

from superwise import logger
from superwise.controller.exceptions import *
from superwise.models.validation_error import ValidationError


class BaseController(ABC):
    """Base class for controllers"""

    __metaclass__ = ABCMeta

    def __init__(self, client, sw):
        """

        :param client: instance of client object (wrapper of requests)
        """
        self.client = client
        self.path = None
        self.model_name = abstractproperty()
        self.logger = logger
        self.model = None
        self.sw = sw

    def _dict_to_model(self, params, model_name=None):
        """

        :param params: dictionary of parameters
        :return: model
        """
        model_name = model_name or self.model_name
        try:
            if "self" in params:
                del params["self"]
            if isinstance(params, list):
                model = list()
                for param in params:
                    cmodel = globals()[model_name](**param)
                    model.append(cmodel)
            else:
                if "__class__" in params:
                    del params["__class__"]
                model = globals()[model_name](**params)
        except Exception as err:
            traceback.print_exc()
            raise Exception("exception in create {}".format(err))
        return model

    def post(self):
        """
        Prepare data and call run API POST call

        :return: requests response object
        """
        params = self.model.get_properties()
        self.logger.info("POST %s ", self.path)
        response = self.client.post(self.build_url(self.path), params)
        return response

    def patch(self, path=None, params=None):
        """
        Prepare data and call run API PATCH call

        :return: requests response object
        """
        path = path or self.path
        params = params or self.model.get_properties()
        self.logger.info("PATCH %s ", self.path)
        res = self.client.patch(self.build_url(path), params)
        return res

    def parse_response(self, response, model_name=None, is_return_model=True):
        """
        Format the response, change it from dict to be model based
        :param r: respnse object (created by requests package)
        :return:
        """
        model_name = model_name or self.model_name
        try:
            body = json.loads(response.content)
        except Exception as ex:
            raise Exception("error loading json, status code {} text {}".format(response.status_code, response.content))
        if response.status_code in [200, 201, 204]:
            res = self._dict_to_model(body, model_name=model_name) if is_return_model else body
        elif response.status_code in [500]:
            response.raise_for_status()
        else:
            res = ValidationError(http_status_code=response.status_code, http_error_reason=response.reason, body=body)
        return res

    def _create_update(self, model, is_return_model=True, create=True, model_name=None, **kwargs):
        """
        create object from an instance of model
        :param model:
        :return:
        """
        action = "create" if create else "update"
        try:
            if model.__class__.__name__ == self.model_name:
                self.model = model
                res = self.post() if create else self.patch()
            else:
                raise Exception(
                    "Model {} passed instead of {} to {}".format(
                        model.__class__.__name__, self.model_name, self.__class__.__name__
                    )
                )

            return self.parse_response(res, is_return_model=is_return_model)
        except SuperwiseValidationException:
            raise
        except Exception as e:
            traceback.print_exc()
            raise Exception("exception in {} {}".format(action, e))

    def create(self, model, return_model=True, **kwargs):
        """
        create object from an instance of model
        :param model:
        :return:
        """
        return self._create_update(model, create=True, return_model=return_model, **kwargs)

    def get(self, fields):
        """
        wrapper for reqeusts.get()

        :param fields: optinal fields for filtering
        :return:  response body string from backend (json)
        """
        self.logger.info("GET %s ", self.path)
        res = self.client.get(self.build_url(self.path), json=fields)
        return res.content

    def get_by_id(self, idx):
        """
        get a specifc resource by id
        :param id:
        :return:
        """
        url = self.build_url("{}/{}".format(self.path, idx))
        self.logger.info("GET  %s ", url)
        res = self.client.get(url)
        return self.parse_response(res)

    def build_url(self, path):
        """
        Build a url for a given path
        :param path: relative path, normally declared in each model (subclasses of this class)

        :return: URL of a resource
        """
        return "https://{}/{}/{}".format(self.client.api_host, self.client.client_name, path)

    def update(self, model, **kwargs):
        """

        :param model: model (instance of any subclass of BaseModel) to update

        """
        return self._create_update(model, create=False, **kwargs)
