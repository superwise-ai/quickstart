""" This module implement data functionality  """
import re

from superwise.controller.base import BaseController
from superwise.controller.exceptions import SuperwiseValidationException


class DataController(BaseController):
    """ Data controller class, implement functionalities for data stream API """

    def __init__(self, client, sw):
        """
        constructer for DataController class

        :param client:

        """
        super().__init__(client, sw)
        self.path = "gateway/v1/file"
        self.model_name = None

    def log_file(self, file_path):
        """
        stream data of a given file path

        :param file_path: url for file stored in cloud str
        :return status bool
        """
        self.logger.info("file_log %s ", file_path)
        pattern = "(s3|gs)://.+"
        if not re.match(pattern, file_path):
            raise SuperwiseValidationException("file_log: file path invalid")
        params = {"file": file_path}
        r = self.client.post(self.build_url("{}".format(self.path)), params)
        self.logger.info("file_log server response: {}".format(r.content))
        if r.status_code == 201:
            return None
        else:
            raise Exception("stream file failed, server error")
