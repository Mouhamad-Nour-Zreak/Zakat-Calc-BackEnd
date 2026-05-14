import collections.abc
collections.Mapping = collections.abc.Mapping
from experta import *
from modules.helpers.helpers import Helper
from modules.zakah.facts import Zakah,Money

# Nisab thresholds
NISAB = {
    "gold": 85.0,     # in grams
    "silver": 595.0   # in grams
}


class MoneyEngine(KnowledgeEngine):
    def __init__(self,_zakah:Zakah):
        super().__init__()
        self._zakah = _zakah

    @DefFacts()
    def _start(self):
        yield self._zakah
        yield Money()

    def get_zakah_fact(self):
        collector = self.facts.popitem()[1]
        while not isinstance(collector, Zakah):
            try:
                collector = self.facts.popitem()[1]
            except:
                return None
        return collector

    def _no_zakah(self,zakah, msg):
        self.modify(zakah,mony={"zakah_value": 0,"details":msg})
        print(msg)
        self.halt()

    @Rule(AS.m << Money(type=None))
    def ask_type(self, m):
        t = Helper.ask("money_type", str)  
        self.modify(m, type=t)

    # ---------------------cash branch ---------------------------

    @Rule(AS.m << Money(type='cash', amount=None))
    def ask_cash_amount(self, m):
        amt = Helper.ask("cash_amount", float)
        debt = Helper.ask("debt_amount",float)
        self.modify(m, amount=amt+debt)

    @Rule(AS.m << Money(type='cash', amount=MATCH.a,nisab_reached = None))
    def check_cash_nisab(self,m, a):
        gold_nisab = NISAB["gold"] * Helper.get_metal_price("XAU")["price_gram_24k"] 
        silver_nisab = NISAB["silver"] * Helper.get_metal_price("XAG")["price_gram_24k"]
        nisab_reached = a >= min(gold_nisab,silver_nisab)
        self.modify(m,nisab_reached = nisab_reached)

    @Rule(Money(type = 'cash',nisab_reached = False),AS.zakah << Zakah())
    def cash_below_nisab(self,zakah):
        self._no_zakah(zakah,"your cash is below nisab, no zakah")

    @Rule(Money(type = 'cash',amount = MATCH.a,nisab_reached = True),AS.zakah << Zakah())
    def cash_zakah(self,a,zakah):
        self.modify(zakah,cash = {
            "total":str(a) + "usd is your total fortune",
            "value": str(a * 0.025) + "usd is your zakah value"
        })
        self.halt()

    # ------------------------------silver and gold branch --------------------

    @Rule(AS.m << Money(type=MATCH.t & L("gold", "silver"), usage=None))
    def ask_usage(self, m):
        u = Helper.ask("gold_and_silver_usage", str)
        self.modify(m, usage=u)

    @Rule(Money(type=MATCH.t & L("gold", "silver"), usage="ornaments"),AS.zakah << Zakah())
    def ornaments_usage(self,zakah):
        self._no_zakah(zakah,"No zakah on precious metals that are used as ornaments")

    @Rule(AS.m << Money(type=MATCH.t & L("gold", "silver"), usage=MATCH.u, weight=None))
    def ask_weight(self, m,t):
        w = Helper.ask("precious_weight",float,f"{t}")
        self.modify(m, weight=w)

    @Rule(
        AS.m << Money(type=MATCH.t, weight=MATCH.w),
        TEST(lambda t, w: w is not None and t in NISAB and w < NISAB[t]),
        AS.zakah << Zakah()
    )
    def metal_below_nisab(self, t,zakah):
        self._no_zakah(zakah,f"Your {t} weight is below Nisab")

    @Rule(
        Money(type=MATCH.Money, usage=MATCH.u, weight=MATCH.w),
        TEST(lambda Money, w: w is not None and Money in NISAB and w >= NISAB[Money]),
        AS.zakah << Zakah(),
    )
    def metal_above_nisab(self, w,zakah):
        self.modify(
            zakah,
            Money={
                "weight": str(w) + " grams",
                "value": str(w * 0.025) + " grams is your zakah",
            },
        )
        self.halt()
