""" This module implement validation errors model  """
from superwise.controller.exceptions import *
from superwise.models.base import BaseModel
 

class ValidationError(BaseModel):
    """ validation error model class, model  for validation errors """

    def __init__(self, http_status_code=None, http_error_reason=None, body=None):
        """

        :param http_status_code: http status code from server
        :param http_error_reason: reason for error
        :param body:jbody of response object
        """
        self.http_status_code = http_status_code
        self.http_error_reason = http_error_reason
        self.details = []
        if isinstance(body, str):
            self.error = body
        else:
            detail = body.get("detail")
            if detail:
                self.error = "Input Validation error"
                if isinstance(detail, list):
                    for item in detail:
                        self.details.append(
                            {
                                "field": ".".join(item["loc"]),
                                "error": "{} in field {}".format(item["msg"], item["loc"][1]),
                            }
                        )
                else:
                    self.details = detail
        raise SuperwiseValidationException(self.get_properties())
