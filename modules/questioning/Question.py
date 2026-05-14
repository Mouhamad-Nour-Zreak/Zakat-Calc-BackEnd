import collections.abc

collections.Mapping = collections.abc.Mapping
from experta import Fact, Field
from .Validator import Validator


class Question(Fact):
    """
    id
    text: question text value
    key: tag value
    validator: anonymous function for making current validation
    
    """
    id = Field(str, True)
    text = Field(str, True)
    key = Field(str, True)
    validator = Field(Validator, True)
