import collections.abc
collections.Mapping = collections.abc.Mapping
from experta import *
from modules.helpers.helpers import Helper
from modules.zakah.facts import *

"""
Expert System for calculating Zakah on Trade Goods,
with a single init rule for all initial prompts.
"""


NISAB = {
    "silver_price": 595.0 * Helper.get_metal_price("XAG")["price_gram_24k"],
    "gold_price": 85.0 * Helper.get_metal_price("XAU")["price_gram_24k"]
}

class TradeOffersEngine(KnowledgeEngine):
    def __init__(self,_zakah:Zakah):
        super().__init__()
        self._zakah = _zakah

    @DefFacts()
    def _start(self):
        yield self._zakah
        yield Trade()
        
            
    def get_zakah_fact(self):
        collector = self.facts.popitem()[1]
        while not isinstance(collector, Zakah):
            try:
                collector = self.facts.popitem()[1]
            except:
                return None
        return collector


    def _no_zakah(self, zakah,msg):
        self.modify(zakah,trade={'zakah_value':0,"description":msg})
        print(msg)
        self.halt()

    @Rule(
        AS.t << Trade(capital=None, stock_value=None, receivables=None,year_passed = None),
        salience=10
    )
    def init(self, t):
        c = Helper.ask("trade_capital", float)
        s = Helper.ask("trade_stock_value", float)
        r = Helper.ask("trade_receivables", float)
        y = Helper.ask("year_passed_on_trade", str) == "y"
        self.modify(t,
            capital=c,
            stock_value=s,
            receivables=r,
            year_passed = y
        )

    @Rule(Trade(year_passed=False),AS.zakah << Zakah(),salience=9)
    def no_zakah_hawl(self,zakah):
        self._no_zakah(zakah,"no zakah, you did not own ur trade one lunar year ago")

    @Rule(
        AS.t << Trade(year_passed=True,capital = MATCH.c,stock_value = MATCH.st,receivables = MATCH.r),
        salience=4
    )
    def reached_nisab(self, t,c,st,r):
        gold_nisab = NISAB["gold_price"]
        silver_nisab = NISAB["silver_price"]
        nisab_reached = st+c+r >= min(gold_nisab,silver_nisab)
        self.modify(t,nisab_reached = nisab_reached)


    @Rule(Trade(nisab_reached=False),AS.zakah << Zakah(),salience=6)
    def no_zakah_nisab(self,zakah):
        self._no_zakah(zakah,"the total of your money is below nisab, no zakah")

    @Rule(Trade(nisab_reached = True,capital = MATCH.c,stock_value = MATCH.st,receivables = MATCH.r),AS.zakah << Zakah(), salience=5)
    def zakah_trade(self,c,st,r,zakah):
        tot = st + r + c
        self.modify(zakah,trade={
            "total": str(tot) + " usd total of the whole trade",
            "value": str(tot * 0.025) + " usd as zakah value"
        })
        self.halt()


