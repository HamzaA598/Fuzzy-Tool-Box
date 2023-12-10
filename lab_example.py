
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
        self.line_equations = self.calculate_line_equations()
        
        
    def calculate_line_equations(self):
        line_equations = []
        for i in range(len(self.values) - 1):
            x1, x2 = self.values[i], self.values[i + 1]
            y1 = 0 if i == 0 else 1
            y2 = 0 if i == len(self.values) - 2 else 1
            
            delta_y = y2 - y1
            delta_x = x2 - x1

            if delta_x == 0: # division by 0 -> slop undefined (parallel to y axis)
                line_equations.append((0, 0))
                continue
            
            slope = delta_y / delta_x
            intercept = y1 - slope * x1
            line_equations.append((slope, intercept))
        return line_equations
                               
class FuzzySystem:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.variables = {}
        self.rules = []
        
    def add_fuzzy_set(self, var_name, set_name, set_type, set_values):
        var = self.variables[var_name]
        for value in set_values:
            if value < var.range[0] or value > var.range[1]:
                #todo SHOW ERROR SOMEHOW
                pass
        fset = Set(set_name, set_type, set_values)
        var.sets.append(fset)     
       
       
       
    def run_simulation(self, crisp_values):
        # fuzzification
        # returns a dict of {variable_name: {set_name: membership}}
        fuzzy_inputs = self.fuzzification(crisp_values)
        # inference
        self.inference()
        # defuzzification
        self.defuzzification()
             
    
    def fuzzification(self, crisp_values):
        
        # helper function to de-nest the code since it was
        # so deeply nested and hurts me
        def fuzzify_variable(var, value):
            membership_values = {}
            for fuzzy_set in var.sets:
                i = -1
                for slope, intercept in fuzzy_set.line_equations:   
                    i += 1
                    # the following if condition makes sure that the crisp value
                    # is within the line points (x1, x2)
                    # if it isnt then it check if the membership of the value was
                    # calculated before if not then it sets it to zero otherwise leave it alone
                    if not (fuzzy_set.values[i] <= value <= fuzzy_set.values[i+1]):
                        if fuzzy_set.name in membership_values:
                            membership = membership_values[fuzzy_set.name]
                        else:
                            membership = 0
                        membership_values[fuzzy_set.name] = membership
                        continue
                    
                    if slope * value + intercept >= 0:
                        membership = max(0, min(1, slope * value + intercept))
                        membership_values[fuzzy_set.name] = membership
            return membership_values
        
        fuzzy_inputs = {}
        for var_name, value in crisp_values.items():
            var = self.variables[var_name]
            if var.type == 1:
                continue # don't need to fuzzify out variables i think?
            fuzzy_inputs[var_name] = fuzzify_variable(var, value)
        return fuzzy_inputs

fuzzy_system = FuzzySystem("Example System", "Testing fuzzy system")

Dirt_variable = variable('Dirt', 'IN', (0, 100))
Fabric_variable = variable('Fabric', 'IN', (0, 100))
wash_variable = variable('Wash', 'OUT', (0, 60))

fuzzy_system.variables['Dirt'] = Dirt_variable
fuzzy_system.variables['Fabric'] = Fabric_variable
fuzzy_system.variables['Wash'] = wash_variable

fuzzy_system.add_fuzzy_set('Dirt', 'Small', 'TRAP', [0, 0, 20, 40])
fuzzy_system.add_fuzzy_set('Dirt', 'Medium', 'TRAP', [20, 40, 60, 80])
fuzzy_system.add_fuzzy_set('Dirt', 'Large', 'TRAP', [60, 80, 100, 100])

fuzzy_system.add_fuzzy_set('Fabric', 'Soft', 'TRAP', [0, 0, 20, 40])
fuzzy_system.add_fuzzy_set('Fabric', 'Ordinary', 'TRAP', [20, 40, 60, 80])
fuzzy_system.add_fuzzy_set('Fabric', 'Stiff', 'TRAP', [60, 80, 100, 100])

fuzzy_system.add_fuzzy_set('Wash', 'very_small', 'TRAP', [0, 0, 15])
fuzzy_system.add_fuzzy_set('Wash', 'small', 'TRAP', [0, 15, 30])
fuzzy_system.add_fuzzy_set('Wash', 'standard', 'TRAP', [15, 30, 45])
fuzzy_system.add_fuzzy_set('Wash', 'large', 'TRAP', [30, 45, 60])
fuzzy_system.add_fuzzy_set('Wash', 'very_large', 'TRAP', [45, 60, 60])

rule_1 = "Dirt Small and Fabric Soft => Wash very_small".split("=>")
rule_2 = "Dirt Medium and Fabric Ordinary => Wash standard".split("=>")
rule_3 = "Dirt Small and not Fabric Soft or Dirt Medium and Fabric Soft => Wash small".split("=>")
rule_4 = "Dirt Medium and Fabric Stiff => Wash large".split("=>")
rule_5 = "Dirt Large and not Fabric Soft => Wash very_large".split("=>")
rule_6 = "Dirt Large and Fabric Soft => Wash standard".split("=>")

fuzzy_system.add_rule(rule_1[0], rule_1[1])
fuzzy_system.add_rule(rule_2[0], rule_2[1])
fuzzy_system.add_rule(rule_3[0], rule_3[1])
fuzzy_system.add_rule(rule_4[0], rule_4[1])
fuzzy_system.add_rule(rule_5[0], rule_5[1])
fuzzy_system.add_rule(rule_6[0], rule_6[1])


crisp_values = {'Dirt': 60, 'Fabric': 25}

fuzzy_inputs = fuzzy_system.run_simulation(crisp_values)
print(f"Fuzzy Inputs: {fuzzy_inputs}")
