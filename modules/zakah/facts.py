import collections.abc

collections.Mapping = collections.abc.Mapping
from experta import *

class Cow(Fact):
    """Fact: Number of cows owned"""
    count = Field(int,False,-1)

class Sheep(Fact):
    """Fact: Number of sheep owned"""
    count  = Field(int,False,-1)

class Money(Fact):
    """
    type: gold, silver, cash
    usage: saving, ornament, others
    weight: for metals, in grams
    amount: for cash, in chosen cash
    """
    type   = Field(str, mandatory=False, default=None)
    nisab_reached = Field(bool, mandatory=False,default=None)
    usage  = Field(str, mandatory=False, default=None)
    weight = Field(float, mandatory=False, default=None)
    amount = Field(float, mandatory=False, default=None)


class Plants(Fact):
    isStaple = Field(bool,mandatory=False)
    cf_staple = Field(float,mandatory=False)
    couldBeStored = Field(bool,mandatory=False)
    cf_stored = Field(float,mandatory=False)
    isRipe = Field(bool,mandatory=False)
    cf_ripe = Field(float,mandatory=False)
    weight = Field(float,mandatory=False)  
    irrigationMethod = Field(str,mandatory=False)

class Trade(Fact):
    capital       = Field(float, mandatory=False, default=None)
    stock_value   = Field(float, mandatory=False, default=None)
    receivables   = Field(float, mandatory=False, default=None)
    year_passed   = Field(bool,  mandatory=False, default=None)
    nisab_reached = Field(bool,mandatory=False,default=None)


class BuriedMoney(Fact):
    """Base fact for any buried wealth."""
    location    = Field(str,   mandatory=False, default=None)
    asset_type  = Field(str,   mandatory=False, default=None)

class Metal(BuriedMoney):
    """Specialized fact for natural metal."""
    metal_type   = Field(str,   mandatory=False, default=None)
    metal_weight = Field(float, mandatory=False, default=None)

class Treasure(BuriedMoney):
    """Specialized fact for buried treasure."""
    pre_islamic    = Field(bool,  mandatory=False, default=None)
    treasure_type  = Field(str,   mandatory=False, default=None)
    treasure_weight= Field(float, mandatory=False, default=None)


#----------------------------camel----------------------------
class Camel(Fact):
    count = Field(int,False,-1)
    pass

class RequiredCamelZakah(Fact):
    type = Field(str)
    amount = Field(int)

class GivenCamel(Fact):
    type = Field(str)
    count = Field(int)

class SubstitutionNeeded(Fact):
    original = Field(str)
    remaining = Field(int)
    current_step = Field(int, default=1)

class SubstitutionProcessed(Fact):
    original = Field(str)
    step = Field(int)
    direction = Field(str)  # "up" or "down"

class Substituted(Fact):
    original = Field(str)
    given = Field(str)
    step = Field(int)
    count = Field(int)
    silver = Field(float)

class Terminate(Fact):
    pass


class Zakah(Fact):
    """Zakah declaration for various assets"""
    sheep = Field(dict, False)
    cows = Field(dict, False)
    camels = Field(dict, False)
    plants = Field(dict,mandatory=False)
    metal = Field(dict, mandatory=False)
    treasure = Field(dict, mandatory=False)
    cash = Field(dict, mandatory=False)
    gold = Field(dict,mandatory=False)
    silver = Field(dict,mandatory=False)
    trade = Field(dict, mandatory=False)
