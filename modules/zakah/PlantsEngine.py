import collections.abc
collections.Mapping = collections.abc.Mapping
from experta import *
from modules.helpers.helpers import Helper
from modules.zakah.facts import *

"""
this engine will determine the zakah of crops and fruits
"""

"""
plants_zakah = "
        weight:
        irrigationMethod:
        value:
    "
"""

cf_map = {
    "certain":1.0,
    "sure":0.8,
    "maybe":0.5,
    "unsure":0.2
}
    

class PlantsEngine(KnowledgeEngine):

    def __init__(self,_zakah:Zakah):
        super().__init__()
        self._zakah = _zakah

    @DefFacts()
    def init(self):
        yield self._zakah
        yield Plants()

    def get_zakah_fact(self):
        collector = self.facts.popitem()[1]
        while not isinstance(collector, Zakah):
            try:
                collector = self.facts.popitem()[1]
            except:
                return None
        return collector

    @Rule(
        AS.plants << Plants(),
        NOT(Plants(isStaple=W())),
        salience=10
    )
    def ask_staple(self,plants):
        isStaple = (Helper.ask("is_it_staple",str)) == "y"
        cf = cf_map[Helper.ask("cf",str)] if isStaple else 0.0   
        self.modify(plants,isStaple = isStaple,cf_staple = cf)

    @Rule(
        AS.plants << Plants(),
        NOT(Plants(couldBeStored=W())),
        salience=9
    )
    def ask_storage(self,plants):
        couldBeStored = (Helper.ask("could_be_stored",str)) == "y"
        self.modify(plants,couldBeStored = couldBeStored)


    @Rule(
        AS.plants << Plants(),
        NOT(Plants(isRipe=W())),
        salience=7
    )
    def ask_ripe(self,plants):
        isRipe = (Helper.ask("is_it_ripe",str)) == "y"
        cf = cf_map[Helper.ask("cf",str)] if isRipe else 0.0   
        self.modify(plants,isRipe = isRipe,cf_ripe = cf)

    @Rule(
        Plants( cf_ripe  = MATCH.cf_ripe & LE(0.2)),
        AS.zakah << Zakah(),
        salience=123
    )
    def wait(self,zakah):
        self.modify(zakah,plants={
            "zakah_value":0,
            "description":"No zakah for unripe plants, u have to wait until it's ripe, then we'll see"
        })
        self.halt()

    @Rule(
        AS.plants << Plants(),
        NOT(Plants(weight=W())),
        salience=5
    )
    def ask_weight(self,plants):
        self.modify(plants,weight = Helper.ask("plants_weight",float))

    @Rule(
        Plants(weight = MATCH.w & LT(653.0)),
        AS.zakah << Zakah(),
        salience=4
    )
    def less_than_nisab(self,w, zakah):
        self.modify(zakah,plants={
            "weight":w,
            "zakah_value":0,
            "description":"No zakah for weight less than 653"
        })
        self.halt()

    @Rule(
        Plants(
            cf_staple = MATCH.cf_staple,
            cf_stored = MATCH.cf_stored
        ),
        TEST(lambda cf_staple,cf_stored:
              (cf_staple + cf_stored * (1 - cf_staple)) <= 0.3
            ),
        AS.zakah << Zakah(),
        salience=8
    )
    def not_conditioned(self,zakah):
        self.modify(zakah,plants={
            "zakah_value":0,
            "description":"Your plants doesn't follow the conditions, the trust is very low"
        })
        self.halt()

    @Rule(
        AS.plants << Plants(),
        NOT(Plants(irrigationMethod = W())),
        salience=3
    )
    def ask_irrigation_method(self,plants):
        self.modify(plants,irrigationMethod = Helper.ask("irrigation",str))

    @Rule(
        AS.plants << Plants(),
        AS.zakah << Zakah()
    )
    def natural_irrigation(self,plants,zakah):
        rates = {'natural': 0.10, 'costly': 0.05, 'mixed': 0.075}
        self.modify(
            zakah,
            plants={
                "weight": str(plants["weight"]) + " kg",
                "irrigationMethod": plants["irrigationMethod"],
                "zakah value": str(plants["weight"] * rates[plants["irrigationMethod"]])
                + " kg",
            },
        )
        self.halt()
