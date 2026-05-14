from modules.questioning.Question import Question
from modules.questioning.Validator import Validator, is_integer,is_float

questions = {
    "cow_count": Question(
        id="cow_count",
        action=lambda string, data: string.format(*data),
        text="How many Cows do you have?",
        key="cow_number",
        choices=[],
        validator=Validator(
            "int", lambda answer: is_integer(answer) and 0 <= int(answer)
        ),
    ),
    "sheep_count": Question(
        id="sheep_count",
        action=lambda string, data: string.format(*data),
        text="How many sheep do you own?",
        key="sheep_number",
        choices=[],
        validator=Validator(
            "int", lambda answer: is_integer(answer) and 0 <= int(answer)
        ),
    ),
    "camels_count": Question(
        id="camels_count",
        action=lambda string, data: string.format(*data),
        text="How many camels do you have?",
        key="camels_number",
        choices=[],
        validator=Validator(
            "int", lambda answer: is_integer(answer) and 0 <= int(answer)
        ),
    ),
    "camel_type_question": Question(
        id="camel_type_question",
        action=lambda string, data: string.format(*data),
        text="How many {0} camels do you have?",
        key="camels_type_number",
        choices=[],
        validator=Validator(
            "int", lambda answer: is_integer(answer) and 0 <= int(answer)
        ),
    ),
    "could_be_stored": Question(
        id="type_of_plants",
        action=lambda string, data: string.format(*data),
        text="could your fruit or crops be stored?",
        key="stored_plants",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "is_it_staple": Question(
        id="is_it_staple",
        action=lambda string, data: string.format(*data),
        text="would you consider your fruit or crops to be staple?",
        key="staple_plants",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "is_it_ripe": Question(
        id="is_it_ripe",
        action=lambda string, data: string.format(*data),
        text="are your fruits and crops ripe?",
        key="ripe_plants",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "plants_weight": Question(
        id="plants_weight",
        action=lambda string, data: string.format(*data),
        text="How much do your crops or fruites weight in kg?",
        key="plants_weight",
        choices=[],
        validator=Validator(
            "float", lambda answer: is_float(answer) and 0.0 <= float(answer)
        ),
    ),
    "irrigation": Question(
        id="irrigation",
        action=lambda string, data: string.format(*data),
        text="what is the method of irrigation?1) natural, for more than 6 months (enter natural)2) costly, for more than 6 months (enter costly)3) mixed, half in half (enter mixed)",
        key="irrigation",
        choices=["natural", "costly", "mixed"],
        validator=Validator(
            "str", lambda answer: answer in ["natural", "costly", "mixed"]
        ),
    ),
    "buried_money_location": Question(
        id="buried_money_location",
        action=lambda string, data: string.format(*data),
        text="where did u find the buried money? 1) Waqf Land or a mosque 2) Property Land 3) Unowned Dead Land ",
        key="buried_money_location",
        choices=["waqf", "property", "dead"],
        validator=Validator(
            "str", lambda answer: answer in ["waqf", "property", "dead"]
        ),
    ),
    "buried_money_asset_type": Question(
        id="buried_money_asset_type",
        action=lambda string, data: string.format(*data),
        text="what's the type of buried money?1) metal in its natural form (enter metal)2) buried treasures (enter treasure)",
        key="buried_money_asset_type",
        choices=["metal", "treasure"],
        validator=Validator("str", lambda answer: answer in ["metal", "treasure"]),
    ),
    "metal_type": Question(
        id="metal_type",
        action=lambda string, data: string.format(*data),
        text="what's the type of the metal or treasure you found?1) Gold (enter gold)2) Silver (enter silver)3) something else (enter else)",
        key="metal_type",
        choices=["silver", "gold", "else"],
        validator=Validator("str", lambda answer: answer in ["silver", "gold", "else"]),
    ),
    "metal_weight": Question(
        id="metal_weight",
        action=lambda string, data: string.format(*data),
        text="how much does your {0} treasure or metal weigh?",
        key="metal_weight",
        choices=[],
        validator=Validator(
            "float", lambda answer: is_float(answer) and 0.0 <= float(answer)
        ),
    ),
    "treasure_age": Question(
        id="treasure_age",
        action=lambda string, data: string.format(*data),
        text="does your treasure dates back to:1) pre-islamic era? enter (yes)2) islamic or unkown era? enter (no)",
        key="treasure_age",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "debt_completing_treasure": Question(
        id="debt_completing_treasure",
        action=lambda string, data: string.format(*data),
        text="Does anyone owe you money in the amount of {0} grams of {1}?",
        key="debt_completing_treasure",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "cattel_ownership": Question(
        id="cattel_ownership",
        action=lambda string, data: string.format(*data),
        text="Do you have any kind of cattels (cows, sheep, camels)?",
        key="cattel_ownership",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "grazing_cattels": Question(
        id="grazing_cattels",
        action=lambda string, data: string.format(*data),
        text="Are your cattles grazing most of the year?",
        key="grazing_cattels",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "buried_mony_ownership": Question(
        id="buried_mony_ownership",
        action=lambda string, data: string.format(*data),
        text="Have you by chance found any burried money? (metals or treasures) y/n",
        key="buried_mony_ownership",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "mony_ownership": Question(
        id="mony_ownership",
        action=lambda string, data: string.format(*data),
        text="Do you have any kind of mony? (Gold, Silver, Cash) y/n",
        key="mony_ownership",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "trade_offers_ownership": Question(
        id="trade_offers_ownership",
        action=lambda string, data: string.format(*data),
        text="Do you have any kind of trade offers? y/n",
        key="trade_offers_ownership",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "plant_ownership": Question(
        id="plant_ownership",
        action=lambda string, data: string.format(*data),
        text="Do you have any kind of corps or fruits? y/n",
        key="plant_ownership",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "debt_completing_treasure": Question(
        id="debt_completing_treasure",
        action=lambda string, data: string.format(*data),
        text="Does anyone owe you money in the amount of {0} grams of {1}?",
        key="debt_completing_treasure",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "trade_capital": Question(
        id="trade_capital",
        action=lambda string, data: string.format(*data),
        text="what's the capital of your trade, money and raw materials value included? (in USD)",
        key="trade_capital",
        choices=[],
        validator=Validator(
            "float", lambda answer: is_float(answer) and 0.0 <= float(answer)
        ),
    ),
    "trade_stock_value": Question(
        id="trade_stock_value",
        action=lambda string, data: string.format(*data),
        text="what's the value of all your trade stocks? (in USD)",
        key="trade_stock_value",
        choices=[],
        validator=Validator(
            "float", lambda answer: is_float(answer) and 0.0 <= float(answer)
        ),
    ),
    "trade_receivables": Question(
        id="trade_receivables",
        action=lambda string, data: string.format(*data),
        text="How much money do people owe you? (in USD)",
        key="trade_receivables",
        choices=[],
        validator=Validator(
            "float", lambda answer: is_float(answer) and 0.0 <= float(answer)
        ),
    ),
    "year_passed_on_trade": Question(
        id="year_passed_on_trade",
        action=lambda string, data: string.format(*data),
        text="Did you own your trade one lunar year ago? )",
        key="year_passed_on_trade",
        choices=["y", "n"],
        validator=Validator("str", lambda answer: answer in ["y", "n"]),
    ),
    "money_type": Question(
        id="money_type",
        action=lambda string, data: string.format(*data),
        text="what is the type of money you got?1) Gold enter (gold) 2) Silver enter (silver)3) Cash (enter cash)",
        key="money_type",
        choices=["gold", "silver", "cash"],
        validator=Validator("str", lambda answer: answer in ["silver", "gold", "cash"]),
    ),
    "cash_amount": Question(
        id="cash_amount",
        action=lambda string, data: string.format(*data),
        text="How much cash do you have?(enter number in usd)",
        key="cash_amount",
        choices=[],
        validator=Validator(
            "float", lambda answer: is_float(answer) and 0.0 <= float(answer)
        ),
    ),
    "debt_amount": Question(
        id="debt_amount",
        action=lambda string, data: string.format(*data),
        text="How much debt do peope owe you?(enter number in usd)",
        key="debt_amount",
        choices=[],
        validator=Validator(
            "float", lambda answer: is_float(answer) and 0.0 <= float(answer)
        ),
    ),
    "gold_and_silver_usage": Question(
        id="gold_and_silver_usage",
        action=lambda string, data: string.format(*data),
        text="What do you use gold and silver for?1) gold women wearables or silver rings for men (enter ornaments)2) I use it for savings or to decorate house - like spoons and bowls (enter savings)",
        key="gold_and_silver_usage",
        choices=["ornaments", "savings"],
        validator=Validator("str", lambda answer: answer in ["ornaments", "savings"]),
    ),
    "precious_weight": Question(
        id="precious_weight",
        action=lambda string, data: string.format(*data),
        text="How much does your {0} weight? (in grams)",
        key="precious_weight",
        choices=[],
        validator=Validator(
            "float", lambda answer: is_float(answer) and 0.0 <= float(answer)
        ),
    ),
    "cf": Question(
        id="cf",
        action=lambda string, data: string.format(*data),
        text="how much are u sure?1) I am very certain (enter certain)2) I am sure (enter sure)3) I think maybe (enter maybe)4) I am not sure (enter unsure)",
        key="cf",
        choices=["certain", "sure", "maybe", "unsure"],
        validator=Validator(
            "str", lambda answer: answer in ["certain", "sure", "maybe", "unsure"]
        ),
    ),
}
