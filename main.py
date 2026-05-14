import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
#from modules.zakah.CowEngine import CowEngine
#from modules.zakah.CamelEngine import CamelEngine
#from modules.zakah.SheepEngine import SheepEngine
#from modules.zakah.PlantsEngine import PlantsEngine
# from modules.zakah.BuriedMoneyEngine import BuriedMoneyEngine
from modules.zakah.MainEngine import MainEngine
from modules.helpers.helpers import Helper



# eng = CowEngine()

# eng = SheepEngine()

# eng = CamelEngine()

 
#eng = PlantsEngine()

eng = MainEngine()

eng.reset()
eng.run()

print(Helper.thaw_frozen(eng.get_zakah_fact()))