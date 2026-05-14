from Collector import Collector
import collections.abc

collections.Mapping = collections.abc.Mapping
from experta import *
from modules.helpers.helpers import Helper
from modules.zakah.facts import *

class CowEngine(KnowledgeEngine):

    def __init__(self,_zakah:Zakah):
        super().__init__()
        self._zakah = _zakah 
        self._collector:Collector = Collector()

    @DefFacts()
    def init(self):
        yield self._zakah
        yield Cow()

    @Rule(
        AS.cow << Cow(count=L(-1))
    )
    def ask_count(self,cow):
        self.modify(cow,count = Helper.ask("cow_count",int))

    @Rule(
        Cow(count=MATCH.count & BETWEEN(0,29)),
        AS.zakah << Zakah()
    )
    def limit_0(self,count,zakah):
        self.modify(zakah,cows={
                "count":count,
                "zakah_value":0,
                "description":"No Zakah in less than 30 cows"
            })
        self.halt()

    # clean rules RHS more to a separate function
    @Rule(
        Cow(count=MATCH.count & BETWEEN(30,39)),
        AS.zakah << Zakah()
    )
    def limit_1(self,count,zakah):
        tabe3 = 1
        self.modify(zakah,cows={
                "count":count,
                "zakah":[{
                    "type":"tabe3",
                    "value":tabe3,
                    "description":f"{tabe3} tabe3, either male or female",
                }]
        })
        self.halt()

    @Rule(
        Cow(count=MATCH.count & BETWEEN(40,59)),
        AS.zakah << Zakah()
    )
    def limit_2(self,count,zakah):
        mosinnah = 1
        self.modify(zakah,cows={
                "count":count,
                "zakah":[{
                    "type":"mosinnah",
                    "value":mosinnah,
                    "description":f"{mosinnah} male or female mosinnah",
                }]
        })
        self.halt()

    @Rule(
        Cow(count=MATCH.count & BETWEEN(60,69)),
        AS.zakah << Zakah()
    )
    def limit_3(self,count,zakah):
        tabe3 = 2
        self.modify(zakah,cows={
                "count":count,
                "zakah":[{
                    "type":"tabe3",
                    "value":tabe3,
                    "description":f"{tabe3} tabe3s, each is either male or female",
                }]
        })
        self.halt()

    @Rule(
        Cow(count=MATCH.count & BETWEEN(70,79)),
        AS.zakah << Zakah()
    )
    def limit_4(self,count,zakah):
        tabe3 = 1
        mosinnah = 1
        self.modify(zakah,cows={
                "count":count,
                "zakah":[{
                    "type":"tabe3",
                    "value":tabe3,
                    "description":f"{tabe3} tabe3, either male or female",
                },{
                    "type":"mosinnah",
                    "value":mosinnah,
                    "description":f"{mosinnah} mosinnah, either male or female",
                }]
        })
        self.halt()

    @Rule(
        Cow(count=MATCH.count & BETWEEN(80,89)),
        AS.zakah << Zakah()
    )
    def limit_5(self,count,zakah):
        mossinah = 2
        self.modify(zakah,cows={
                "count":count,
                "zakah":[{
                    "type":"mossinah",
                    "value":mossinah,
                    "description":f"{mossinah} mossinah, each is either male or female",
                }]
        })
        self.halt()

    @Rule(
        Cow(count=MATCH.count & BETWEEN(90,99)),
        AS.zakah << Zakah()
    )
    def limit_6(self,count,zakah):
        tabe3 = 3
        self.modify(zakah,cows={
                "count":count,
                "zakah":[{
                    "type":"tabe3",
                    "value":tabe3,
                    "description":f"{tabe3} tabe3s, each is either male or female",
                }]
        })
        self.halt()

    @Rule(
        Cow(count=MATCH.count & BETWEEN(100,109)),
        AS.zakah << Zakah()
    )
    def limit_7(self,count,zakah):
        tabe3 = 2
        mosinnah = 1
        self.modify(zakah,cows={
                "count":count,
                "zakah":[{
                    "type":"tabe3",
                    "value":tabe3,
                    "description":f"{tabe3} tabe3s, each is either male or female",
                },{
                    "type":"mosinnah",
                    "value":mosinnah,
                    "description":f"{mosinnah} mosinnah, either male or female",
                }]
        })
        self.halt()

    @Rule(
        Cow(count=MATCH.count & BETWEEN(110,119)),
        AS.zakah << Zakah()
    )
    def limit_8(self,count,zakah):
        tabe3 = 1
        mosinnah = 2
        self.modify(zakah,cows={
                "count":count,
                "zakah":[{
                    "type":"tabe3",
                    "value":tabe3,
                    "description":f"{tabe3} tabe3, either male or female",
                },{
                    "type":"mosinnah",
                    "value":mosinnah,
                    "description":f"{mosinnah} mosinnahs, each is either male or female",
                }]
        })
        self.halt()

    @Rule(
        Cow(count=MATCH.count & GE(120)),
        AS.zakah << Zakah()
    )
    def limit_9(self,count,zakah):
        mosinnah = (count % 30)//10
        tabe3 = count//30 - mosinnah

        self.modify(zakah,cows={
                "count":count,
                "zakah":[{
                    "type":"tabe3",
                    "value":tabe3,
                    "description":f"{tabe3} tabe3s, each is either male or female",
                },{
                    "type":"mosinnah",
                    "value":mosinnah,
                    "description":f"{mosinnah} mosinnahs, each is either male or female",
                }]
        })
        self.halt()

    def get_collector(self):
        return self._collector

    def get_zakah_fact(self):
        collector = self.facts.popitem()[1]
        while not isinstance(collector, Zakah):
            try:
                collector = self.facts.popitem()[1]
            except:
                return None
        return collector
