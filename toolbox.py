from enum import Enum

class variable:
    
    def __init__(self, name, type, v_range):
        self.name = name
        self.type = 0 if type.upper() == "IN" else 1
        self.range = v_range
        self.sets = []
    
    