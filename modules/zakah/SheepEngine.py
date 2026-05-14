import collections.abc
collections.Mapping = collections.abc.Mapping
from experta import *
from modules.helpers.helpers import Helper
from modules.zakah.facts import *


"""
shape of zakah dict

sheep = {
    sheep_count:
    zakah_value:
    description:
}
"""

class SheepEngine(KnowledgeEngine):
    def __init__(self,_zakah:Zakah):
        super().__init__()
        self._zakah = _zakah 
      
    @DefFacts()
    def init(self):
        yield self._zakah
        yield Sheep()
        
    def get_zakah_fact(self):
        collector = self.facts.popitem()[1]
        while not isinstance(collector, Zakah):
            try:
                collector = self.facts.popitem()[1]
            except:
                return None
        return collector

    @Rule(
        AS.sheep << Sheep(count=L(-1))
    )
    def ask_count(self,sheep):
        self.modify(sheep,count = Helper.ask("sheep_count",int))

    @Rule(
        Sheep(
            count = MATCH.count &  BETWEEN(0,39)
        ),
        AS.zakah << Zakah()
    )
    def limit_0(self,count,zakah):
        self.modify(zakah,sheep=
                           {"sheep_count":count,
                            "zakah_value":0,
                            "description":"No Zakah in less than 40 sheeps"}),
        self.halt()

    @Rule(
        Sheep(
            count = MATCH.count &  BETWEEN(40,120)
        ),
        AS.zakah << Zakah()
    )
    def limit_1(self,count,zakah):
        self.modify(zakah,sheep=
                           {"sheep_count":count,
                           "zakah_value":1,
                           "description":"1 year old dah'n or 2 years old goat"}),
        self.halt()

    @Rule(
        Sheep(
            count = MATCH.count &  BETWEEN(121,200)
        ),
        AS.zakah << Zakah()
    )
    def limit_2(self,count,zakah):
        self.modify(zakah,sheep=
                           {"sheep_count":count,
                            "zakah_value":2,
                            "description":"each is either 1 year old dah'n or 2 years old goat"}),
        self.halt()

    @Rule(
        Sheep(
            count = MATCH.count &  BETWEEN(201,399)
        ),
        AS.zakah << Zakah()
    )
    def limit_3(self,count,zakah):
        self.modify(zakah,sheep=
                           {"sheep_count":count,
                            "zakah_value":3,
                            "description":"each is either 1 year old dah'n or 2 years old goat"}),
        self.halt()

    @Rule(
        Sheep(
            count = MATCH.count &  GE(400)
        ),
        AS.zakah << Zakah()
    )
    def limit_4(self,count,zakah):
        self.modify(zakah,sheep=
                           {"sheep_count":count,
                            "zakah_value":count//100,
                            "description":"each is either 1 year old dah'n or 2 years old goat"}),
        self.halt()

