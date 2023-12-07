class variable:
    def __init__(self, name, type, v_range):
        self.name = name
        self.type = 0 if type.upper() == "IN" else 1
        self.range = v_range
        self.sets = []
    
class Set:
    def __init__(self, name, ftype, values):
        self.name = name
        self.type = ftype
        self.values = values
        self.center = sum(values) / len(values)
        
class FuzzySystem:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.variables = {}
        self.rules = []
        
    def add_variable(self):
        pass
    
    def add_fuzzy_set(self, var_name, set_name, set_type, set_values):
        var = self.variables[var_name]
        for value in set_values:
            if value < var.range[0] or value > var.range[1]:
                #todo SHOW ERROR SOMEHOW
                pass
        fset = Set(set_name, set_type, set_values)
        var.sets.append(fset)
    
    def add_rule(self):
        pass
    
    def run_simulation(self):
        pass

def main():
    print("Fuzzy Logic Toolbox")
    print("===================")
    print("1- Create a new fuzzy system.")
    print("2- Quit.")
    user_input = input()
    
    if user_input == "2":
        return
    
    print("Enter the system's name and a brief description:")
    system_name = input()
    system_description = input()
    fuzzy_system = FuzzySystem(system_name, system_description)
    
    while True:
        print("\nMain Menu:")
        print("==========")
        print("1- Add variables.")
        print("2- Add fuzzy sets to an existing variable.")
        print("3- Add rules.")
        print("4- Run the simulation on crisp values.")
        print("-----------------------------")
        
        user_input = input()
        
        if user_input == "1":
            #todo variables input
            pass
        elif user_input == "2":
            print("Enter the variable's name:")
            var_name = input()
            print("Enter the fuzzy set name, type (TRI/TRAP), and values: (Press x to finish)")
            
            while True:
                set_input = input().split()
                if set_input[0] == 'x':
                    break
                set_name, set_type, *set_values = set_input
                set_values = list(map(int, set_values))
                fuzzy_system.add_fuzzy_set(var_name, set_name, set_type, set_values)
        elif user_input == "3":
            #todo rules input
            pass
        elif user_input == "4":
            #todo crisp input and simulation
            break


if __name__ == "__main__":
    main()