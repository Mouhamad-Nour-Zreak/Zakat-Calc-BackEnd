import collections.abc

collections.Mapping = collections.abc.Mapping
from experta import Field , Fact


class Answer(Fact):
    question_id = Field(str, True)
    value = Field(str, True)
    key = Field(str, True)
