import collections.abc
from Collector import Collector
collections.Mapping = collections.abc.Mapping
from experta import *
from modules.helpers.helpers import Helper
from modules.zakah.facts import *

"""
shape of zakah dict

camels_zakah : {
    camels_count:
    zakah:[
        {
            value:
            description:
        }
    ],
    compensations: f"{comp} silver gram"
}
"""

# Constants
CAMEL_LADDER = [
    "Ibn Laboon",
    "Bint Makhaad",
    "Bint Laboon",
    "Haqah",
    "Jath3a",
    "Thanya"
]

class CamelEngine(KnowledgeEngine):

    def __init__(self,_zakah):
        super().__init__()
        self._zakah = _zakah
        self._collector:Collector = Collector()

    @DefFacts()
    def init(self):
        yield self._zakah
        yield Camel()
        
    def get_zakah_fact(self):
        collector = self.facts.popitem()[1]
        while not isinstance(collector, Zakah):
            try:
                collector = self.facts.popitem()[1]
            except:
                return None
        return collector

    
    @Rule(
        AS.camel << Camel(count=L(-1))
    )
    def ask_count(self,camel):
        self.modify(camel,count = Helper.ask("camels_count",int))

#--------------------------------------------------------------------------------------
#limits
    @Rule(
        Camel(
            count = MATCH.count & BETWEEN(0,4)
        ),
        AS.zakah << Zakah()
    )
    def limit_0(self,count,zakah):
        self.modify(zakah,camels = 
                           {"camels_count":count,
                            "zakah":[
                                {
                                    "value":0,
                                    "description":"no zakah in less than 5 camels"
                                }
                            ]})
        self.halt()
    
    @Rule(
        Camel(
            count = MATCH.count & BETWEEN(5,26)
        ),
        AS.zakah << Zakah()
    )
    def limit_1(self,count,zakah):
        self.modify(zakah,camels = 
                           {"camels_count":count,
                            "zakah":[
                                {
                                    "value":count//5,
                                    "description":"sheep, either dah'n Jath3a or goat Thanya"
                                }
                            ]})
        self.halt()

    @Rule(
        Camel(
            count = MATCH.count & BETWEEN(26,35)
        )
    )
    def limit_2(self):
        self.declare(RequiredCamelZakah(type = "Bint Makhaad",amount = 1))
    

    @Rule(
        Camel(
            count = MATCH.count & BETWEEN(36,45)
        )
    )
    def limit_3(self,zakah):
        self.declare(RequiredCamelZakah(type = "Bint Laboon",amount = 1))
    

    @Rule(
        Camel(
            count = MATCH.count & BETWEEN(46,60)
        )
    )
    def limit_4(self):
        self.declare(RequiredCamelZakah(type = "Haqah",amount = 1))
    

    @Rule(
        Camel(
            count = MATCH.count & BETWEEN(61,75)
        )
    )
    def limit_5(self):
        self.declare(RequiredCamelZakah(type = "Jath3a",amount = 1))

    @Rule(
        Camel(
            count = MATCH.count & BETWEEN(76,90)
        )
    )
    def limit_6(self):
        self.declare(RequiredCamelZakah(type = "Bint Laboon",amount = 2))

    @Rule(
        Camel(
            count = MATCH.count & BETWEEN(91,119)
        )
    )
    def limit_7(self):
        self.declare(RequiredCamelZakah(type = "Haqah",amount = 2))

    @Rule(
        Camel(
            count = MATCH.count & GE(120)
        )
    )
    def limit_8(self,count):
        Haqah_count = int((count%40)/10)
        Bint_Laboon_count = int(count//40 - Haqah_count)
        if(Haqah_count!= 0): 
            self.declare(RequiredCamelZakah(type = "Haqah",amount = Haqah_count))
        self.declare(RequiredCamelZakah(type = "Bint Laboon",amount = Bint_Laboon_count))

#---------------------------------------------------------------------------------------------

    @Rule(
        RequiredCamelZakah(
            type=MATCH.type, amount=MATCH.amount
        )
    )
    def ask_user_has_type(self, type, amount):
        user_count = Helper.ask("camel_type_question",int,f"{type}")
        self.declare(GivenCamel(type=type, count=min(user_count, amount)))

    @Rule(
        RequiredCamelZakah(
            type=MATCH.typ, amount=MATCH.amount
        ),
        GivenCamel(
            type=MATCH.typ, count=MATCH.count
        ),
        TEST(lambda count, amount: count < amount)
    )
    def initiate_substitution(self, typ, amount, count):
        remaining = amount - count
        self.declare(SubstitutionNeeded(original=typ, remaining=remaining, current_step=1))

 

    # Rule to try substitution going UP first
    @Rule(
        AS.sub_needed << SubstitutionNeeded(
            original=MATCH.original, remaining=MATCH.remaining, current_step=MATCH.step
        ),
        NOT(SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="up")),
        TEST(lambda original, step: CAMEL_LADDER.index(original) + step < len(CAMEL_LADDER))
    )
    def try_substitute_up(self, sub_needed, original, remaining, step):
        idx = CAMEL_LADDER.index(original)
        candidate = CAMEL_LADDER[idx + step]
        
        user_count = Helper.ask("camel_type_question", int, f"{candidate}")
        actual = min(user_count, remaining)
        silver = round(actual * step * -6.25, 2)
        
        self.declare(SubstitutionProcessed(original=original, step=step, direction="up"))
        
        if actual > 0:
            self.declare(GivenCamel(type=candidate, count=actual))
            self.declare(Substituted(original=original, given=candidate, step=step, count=actual, silver=silver))
            
            new_remaining = remaining - actual
            if new_remaining > 0:
                self.modify(sub_needed, remaining=new_remaining)
            else:
                self.retract(sub_needed)

    # Rule to try substitution going DOWN after UP is processed
    @Rule(
        AS.sub_needed << SubstitutionNeeded(
            original=MATCH.original, remaining=MATCH.remaining, current_step=MATCH.step
        ),
        SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="up"),
        NOT(SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="down")),
        TEST(lambda original, step: CAMEL_LADDER.index(original) - step >= 0)
    )
    def try_substitute_down(self, sub_needed, original, remaining, step):
        idx = CAMEL_LADDER.index(original)
        candidate = CAMEL_LADDER[idx - step]
        
        user_count = Helper.ask("camel_type_question", int, f"{candidate}")
        actual = min(user_count, remaining)
        silver = round(actual * step * 6.25, 2)
        
        self.declare(SubstitutionProcessed(original=original, step=step, direction="down"))
        
        if actual > 0:
            self.declare(GivenCamel(type=candidate, count=actual))
            self.declare(Substituted(original=original, given=candidate, step=step, count=actual, silver=silver))
            
            new_remaining = remaining - actual
            if new_remaining > 0:
                self.modify(sub_needed, remaining=new_remaining)
            else:
                self.retract(sub_needed)

    # Rule to move to next step after both up and down are processed
    @Rule(
        AS.sub_needed << SubstitutionNeeded(
            original=MATCH.original, remaining=MATCH.remaining, current_step=MATCH.step
        ),
        SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="up"),
        SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="down"),
        TEST(lambda remaining: remaining > 0)
    )
    def move_to_next_step(self, sub_needed, original, remaining, step):
        self.modify(sub_needed, current_step=step + 1)

    # Rule to handle case where UP is not possible but DOWN is
    @Rule(
        AS.sub_needed << SubstitutionNeeded(
            original=MATCH.original, remaining=MATCH.remaining, current_step=MATCH.step
        ),
        NOT(SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="up")),
        NOT(SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="down")),
        TEST(lambda original, step: CAMEL_LADDER.index(original) + step >= len(CAMEL_LADDER)),
        TEST(lambda original, step: CAMEL_LADDER.index(original) - step >= 0)
    )
    def skip_up_try_down(self, sub_needed, original, remaining, step):
        self.declare(SubstitutionProcessed(original=original, step=step, direction="up"))

    # Rule to handle case where DOWN is not possible but UP is
    @Rule(
        AS.sub_needed << SubstitutionNeeded(
            original=MATCH.original, remaining=MATCH.remaining, current_step=MATCH.step
        ),
        SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="up"),
        NOT(SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="down")),
        TEST(lambda original, step: CAMEL_LADDER.index(original) - step < 0)
    )
    def skip_down_move_next(self, sub_needed, original, remaining, step):
        self.declare(SubstitutionProcessed(original=original, step=step, direction="down"))

    # Rule to handle case where neither UP nor DOWN is possible
    @Rule(
        AS.sub_needed << SubstitutionNeeded(
            original=MATCH.original, remaining=MATCH.remaining, current_step=MATCH.step
        ),
        NOT(SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="up")),
        NOT(SubstitutionProcessed(original=MATCH.original, step=MATCH.step, direction="down")),
        TEST(lambda original, step: CAMEL_LADDER.index(original) + step >= len(CAMEL_LADDER)),
        TEST(lambda original, step: CAMEL_LADDER.index(original) - step < 0)
    )
    def skip_both_directions(self, original, step):
        self.declare(SubstitutionProcessed(original=original, step=step, direction="up"))
        self.declare(SubstitutionProcessed(original=original, step=step, direction="down"))


    @Rule(
        NOT(SubstitutionNeeded()),
        AS.zakah << Zakah() 
    )
    def finalize(self,zakah):
        camel_count = 0
        zakah_list = []
        total_silver = 0

        # Search for the Camel fact to get the count
        for fact in self.facts.values():
            if isinstance(fact, Camel):
                camel_count = fact['count']
                break

        # Collect all GivenCamels and Substituted silver values
        for fact in self.facts.values():
            if isinstance(fact, GivenCamel):
                zakah_list.append({
                    "value": fact["count"],
                    "description": fact["type"]
                })
            if isinstance(fact, Substituted):
                total_silver += fact["silver"]

        zakah_data = {
            "camels_count": camel_count,
            "zakah": zakah_list,
            "compensations": f"{total_silver} silver gram or {int(total_silver/6.25)} sheep"
        }
        self.modify(zakah,camels=zakah_data)
        self.halt()
