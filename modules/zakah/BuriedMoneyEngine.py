import collections.abc
collections.Mapping = collections.abc.Mapping
from experta import *
from modules.helpers.helpers import Helper
from modules.zakah.facts import *

"""
Expert System for calculating Zakah on buried metals and treasures.
"""

# Thresholds (in grams)
NISAB = {
    'gold': 85,
    'silver': 595,
}



class BuriedMoneyEngine(KnowledgeEngine):
    def __init__(self, _zakah:Zakah):
        super().__init__()
        self._zakah = _zakah
        
    @DefFacts()
    def init(self):
        # start with generic buried money
        yield self._zakah
        yield BuriedMoney()
        
    def get_zakah_fact(self):
        collector = self.facts.popitem()[1]
        while not isinstance(collector, Zakah):
            try:
                collector = self.facts.popitem()[1]
            except:
                return None
        return collector
        

    def _lost_property_ruling(self,zakah, msg="buried money is subject to the same ruling as lost property."):
        print(msg)
        self.modify(zakah,treasure={"zakah_value":0,"description":msg})
        self.halt()

    def _no_zakah(self,zakah, msg):
        print(msg)
        self.modify(zakah,treasure={"zakah_value":0,"description":msg})
        self.halt()

    # 1. Ask location
    @Rule(AS.bm << BuriedMoney(location=None), salience=11)
    def ask_location(self, bm):
        ans = Helper.ask("buried_money_location",str)
        self.modify(bm, location=ans)

    @Rule(BuriedMoney(location='waqf'),AS.zakah << Zakah())
    def rule_waqf(self,zakah):
        self._lost_property_ruling(zakah)

    @Rule(BuriedMoney(location='property'),AS.zakah << Zakah())
    def rule_owned(self,zakah):
        self._no_zakah(zakah,"The treasure belongs to the landowner")

    @Rule(AS.bm << BuriedMoney(location='dead', asset_type=None), salience=10)
    def ask_asset_type(self, bm):
        ans = Helper.ask("buried_money_asset_type",str)
        self.modify(bm, asset_type=ans)

    # Metal branch: downcast
    @Rule(AS.bm << BuriedMoney(asset_type='metal'))
    def to_metal(self, bm):
        self.declare(Metal(location=bm['location']))
        self.retract(bm)

    # Treasure branch: downcast
    @Rule(AS.bm << BuriedMoney(asset_type='treasure'))
    def to_treasure(self, bm):
        self.declare(Treasure(location=bm['location']))
        self.retract(bm)

    # ----- Metal rules -----
    @Rule(AS.m << Metal(metal_type=None), salience=9)
    def ask_metal_type(self, m):
        ans = Helper.ask("metal_type",str)  
        self.modify(m, metal_type=ans)

    @Rule(Metal(metal_type='else'),AS.zakah << Zakah(),salience=8)
    def no_zakah_other_metal(self,zakah):
        self._no_zakah(zakah, "No zakah in metals other than silver or gold")

    @Rule(AS.m << Metal(metal_type=MATCH.mt, metal_weight=None), salience=7)
    def ask_metal_weight(self,mt, m):
        w = Helper.ask("metal_weight",float,f"{mt}")
        self.modify(m, metal_weight=w)

    @Rule(Metal(metal_type=MATCH.mt, metal_weight=MATCH.w), TEST(lambda mt,w: mt in NISAB and w is not None and w < NISAB[mt]),AS.zakah << Zakah())
    def metal_below_nisab(self,zakah):
        self._no_zakah(zakah,"Nisab unreached in metal no zakah")

    @Rule(Metal(metal_type=MATCH.mt, metal_weight=MATCH.w), TEST(lambda mt,w: mt in NISAB and w is not None and w >= NISAB[mt]),AS.zakah << Zakah())
    def metal_zakah(self, w,mt,zakah):
        amount = w * 0.025
        self.modify(zakah, metal={"weight":w,"value":str(amount)+ f" grams of {mt}"})
        self.halt()
        # self.declare(Zakah(metal={"weight": w, "value": str(amount) + f" grams of {mt}"}))

    # ----- Treasure rules -----
    @Rule(AS.t << Treasure(pre_islamic=None), salience=9)
    def ask_treasure_age(self, t):
        ans = Helper.ask("treasure_age",str)
        self.modify(t, pre_islamic=(ans == "y"))

    @Rule(Treasure(pre_islamic=False),AS.zakah << Zakah(),salience=8)
    def treasure_post(self,zakah):
        self._lost_property_ruling(zakah)

    @Rule(AS.t << Treasure(pre_islamic=True, treasure_type=None), salience=7)
    def ask_treasure_type(self, t):
        ans = Helper.ask("metal_type",str)
        self.modify(t, treasure_type=ans)

    @Rule(Treasure(treasure_type='else'),AS.zakah << Zakah(),salience=6)
    def no_zakah_other_treasure(self,zakah):
        # self.modify(zakah,treaser={"type":"else","description":"there is no zakah in treasure unless it's silver or gold"})
        self._no_zakah(zakah,"there is no zakah in treasure unless it's silver or gold")
        self.halt()

    @Rule(AS.t << Treasure(treasure_type=MATCH.tt, treasure_weight=None), salience=5)
    def ask_treasure_weight(self, t, tt):
        w = Helper.ask("metal_weight",float,f"{tt}")
        self.modify(t, treasure_weight=w)

    @Rule(Treasure(treasure_type=MATCH.tt, treasure_weight=MATCH.w), TEST(lambda tt,w: w is not None and tt in NISAB and w < NISAB[tt]),AS.zakah << Zakah())
    def treasure_below_nisab(self,w,zakah):
        # self.modify(zakah,treaser={"weight":w,"description":"you treasure is below nisab, there is no zakah"})
        self._no_zakah(zakah,"you treasure is below nisab, there is no zakah")

    @Rule(Treasure(treasure_type=MATCH.tt, treasure_weight=MATCH.w), TEST(lambda tt,w: w is not None and tt in NISAB and w >= NISAB[tt]),AS.zakah << Zakah())
    def treasure_zakah(self, tt, w,zakah):
        amount = w * 0.025
        self.modify(zakah,treasure={"weight": w, "value": str(amount) + f" grams of {tt}"})
        self.halt()
        # self.declare(Zakah(treasure={"weight": w, "value": str(amount) + f" grams of {tt}"}))