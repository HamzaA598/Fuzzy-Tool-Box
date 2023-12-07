class FuzzySystem:
    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description
        self.variables = []
        self.rules = []
        
    def add_variable():
        pass
    
    def add_fuzzy_set():
        pass
    
    def add_rule():
        pass


class Set:
    def __init__(self, name, ftype, values):
        self.name = name
        self.type = ftype
        self.values = values
        self.center = sum(values) / len(values)
        
def main():
    print("Fuzzy Logic Toolbox")
    print("===================")
    print("1- Create a new fuzzy system.")
    print("2- Quit.")
    user_input = input()
    if user_input == "1":
        print("Enter the system’s name and a brief description:")
        system_name = input()
        system_description = input()
        fuzzy_system = FuzzySystem(system_name, system_description)
    else:
        return
    
    



if __name__ == "__main__":
    main()