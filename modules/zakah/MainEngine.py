import collections.abc
collections.Mapping = collections.abc.Mapping

from experta import *
from modules.helpers.helpers import Helper
from modules.zakah.CamelEngine import CamelEngine
from modules.zakah.SheepEngine import SheepEngine
from modules.zakah.CowEngine import CowEngine
from modules.zakah.PlantsEngine import PlantsEngine
from modules.zakah.BuriedMoneyEngine import BuriedMoneyEngine
from modules.zakah.MoneyEngine import MoneyEngine
from modules.zakah.TradeOffersEngine import TradeOffersEngine
from modules.zakah.facts import Zakah

class UserState(Fact):
    pass

class MainEngine(KnowledgeEngine):

    @DefFacts()
    def init(self):
        yield Zakah()
        yield UserState()

    def finishZakatCalc(self):
        from link.state import state_manager
        zakat = Helper.thaw_frozen(dict(**self.get_zakah_fact()))
        state_manager.question_ready.set()
        state_manager.is_finished = True
        state_manager.final_zakah = zakat
        self.halt()

    def get_zakah_fact(self):
        collector = self.facts.popitem()[1]
        while not isinstance(collector, Zakah):
            try:
                collector = self.facts.popitem()[1]
            except:
                return None
        return collector

    @Rule(
        AS.user_state << UserState(),
        NOT(UserState(has_trade_offers=W())),
        salience=8
    )
    def ask_trade_offers_ownership(self,user_state):
        ans = Helper.ask("trade_offers_ownership")
        self.modify(user_state,has_trade_offers=(ans == 'y'))

    @Rule(
        AS.user_state << UserState(),
        NOT(UserState(has_cattels=W())),
        salience=7
    )
    def ask_cattel_ownership(self,user_state):
        ans = Helper.ask("cattel_ownership")
        self.modify(user_state,has_cattels=(ans == 'y'))

    @Rule(
        AS.user_state << UserState(has_cattels=L(True)),
        NOT(UserState(cattels_grazing_most_year=W())),
        salience=6
    )
    def ask_cattel_grazing_state(self,user_state):
        ans = Helper.ask("grazing_cattels")
        self.modify(user_state,cattels_grazing_most_year=(ans == 'y'))

    @Rule(
        AS.user_state << UserState(),
        NOT(UserState(has_mony=W())),
        salience=5
    )
    def ask_mony_ownership(self,user_state):
        ans = Helper.ask("mony_ownership")
        self.modify(user_state,has_mony=(ans == 'y'))

    @Rule(
        AS.user_state << UserState(),
        NOT(UserState(has_buried_mony=W())),
        salience=4
    )
    def ask_buried_mony_ownership(self,user_state):
        ans = Helper.ask("buried_mony_ownership")
        self.modify(user_state,has_buried_mony=(ans == 'y'))

    @Rule(
        AS.user_state << UserState(),
        NOT(UserState(has_plants=W())),
        salience=3
    )
    def ask_plant_ownership(self,user_state):
        ans = Helper.ask("plant_ownership")
        self.modify(user_state,has_plants=(ans == 'y'))

    @Rule(
        AS.user_state << UserState(has_cattels=L(True), cattels_grazing_most_year=L(True)),
        AS.zakah << Zakah(),
        salience=2
    )
    def cattel_details(self,user_state,zakah):
        eng = CamelEngine(zakah)
        eng.reset()
        eng.run()
        eng = CowEngine(Zakah(**eng.get_zakah_fact()))
        eng.reset()
        eng.run()
        eng = SheepEngine(Zakah(**eng.get_zakah_fact()))
        eng.reset()
        eng.run()
        self.modify(zakah, **eng.get_zakah_fact())
        self.modify(user_state, has_cattels=False)

    @Rule(
        AS.user_state << UserState(has_plants=L(True)),
        AS.zakah << Zakah(),
        salience=1
    )
    def plant_details(self,user_state,zakah):
        eng = PlantsEngine(zakah)
        eng.reset()
        eng.run()
        self.modify(user_state, has_plants=False)
        self.modify(zakah,**eng.get_zakah_fact())

    @Rule(
        AS.user_state << UserState(has_mony=L(True)),
        AS.zakah << Zakah(),
        salience=0
    )
    def mony_details(self,user_state,zakah):
        eng = MoneyEngine(zakah)
        eng.reset()
        eng.run()
        self.modify(zakah,**eng.get_zakah_fact())
        self.modify(user_state,has_mony=False)

    @Rule(
        AS.user_state << UserState(has_trade_offers=L(True)),
        AS.zakah << Zakah(),
        salience=-1
    )
    def trade_offers_details(self,user_state,zakah):
        eng = TradeOffersEngine(zakah)
        eng.reset()
        eng.run()
        self.modify(zakah,**eng.get_zakah_fact())
        self.modify(user_state,has_trade_offers=False)

    @Rule(
        AS.user_state << UserState(has_buried_mony=L(True)),
        AS.zakah << Zakah(),
        salience=-2
    )
    def buried_mony_details(self,user_state,zakah):
        eng = BuriedMoneyEngine(zakah)
        eng.reset()
        eng.run()
        self.modify(zakah,**eng.get_zakah_fact())
        self.modify(user_state,has_buried_mony=False)

    @Rule(
        AS.user_state
        << UserState(has_cattels=L(False), has_plants=L(False), has_mony=L(False)),
        salience=-3,
    )
    def finish(self, user_state):
        self.finishZakatCalc()
