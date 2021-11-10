""" This module implement data custom exceptions  """
 

class SuperWiseValidationError(Exception):
    """  SuperWiseValidationError customn exception """


class SuperwiseException(SuperWiseValidationError):
    """  SuperwiseException customn exception """


class SuperwiseValidationException(SuperWiseValidationError):
    """  SuperwiseValidationException customn exception """


class SuperwiseAuthException(SuperWiseValidationError):
    """  SuperwiseAuthException customn exception """
