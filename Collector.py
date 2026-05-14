# store answers of the Questions
# In general: a class to communicate between layers
class Collector:
    def __init__(self):
        self._data = {}

    
    def set_data(self , data :dict):
        self._data = data
    
    def get_data(self):
        return self._data
    
    def append(self , key , value):
        self._data[key] = value
        
    def get(self, key):
        return self._data.get(key)
    
    def key_exists(self, key):
        return key in self._data