""" This module contain BaseModel class  """
import datetime
from enum import Enum
 

class BaseModel:
    """ Base model """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)

    def from_datetime(self, date):
        if not date:
            return None
        elif isinstance(date, datetime.datetime):
            return date.isoformat()
        else:
            return date

    def get_properties(self):

        """
        get properrties of model as dictionary

        :return: properties dict
        """
        return dict(
            (name, getattr(self, name))
            for name in dir(self)
            if not name.startswith("__") and not callable(getattr(self, name))
        )

    def get_enum_value(self, v):
        if isinstance(v, Enum):
            return v.value
        else:
            return v
