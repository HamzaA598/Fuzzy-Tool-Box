# node class for rules' tree
class Node:
    def __init__(self, value, var_set = None):
        self.value = value
        self.left_child = None
        self.right_child = None
        self.var_set = var_set

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

            if delta_x == 0: # division by 0 -> slope undefined
                line_equations.append((0, 0))
                continue
            
            slope = delta_y / delta_x
            intercept = y1 - slope * x1
            line_equations.append((slope, intercept))
        return line_equations
        
class Rule:
    def __init__(self, in_tree, out_var, out_set):
        self.in_tree = in_tree
        self.out_var = out_var
        self.out_set = out_set
    
    # function to print the tree incase you want to see how the rule looks
    def print_rule(self, node, level=0):
        if node is not None:
            print("  " * level + str(node.value), end=" ")
            if node.var_set is not None:
                print(f"({node.var_set})", end=" ")
            print()
            self.print_rule(node.left_child, level + 1)
            self.print_rule(node.right_child, level + 1)

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
    
    #! is this correct????????????????
    #! not sure if overcomplicating or not
    #! add_rule function creates a syntax tree for the rule evaluation
    #! check test.py for testing the rule creation with examples
    def add_rule(self, rule_in_str, rule_out_str):
        rule_in_str = rule_in_str.replace('NOT ', '~')
        rule_out = rule_out_str.split()
        tokens = rule_in_str.split()

        # define the operators and their precedence
        # not sure if and is first or or is first
        # currently assumes or is done first (lower in the tree)
        operators = {'AND': 1, 'OR': 2}

        # function to create the syntax tree for the rule
        # checks for the operators first if there isn't one it create a terminal node
        def build_tree(tokens):
            if not tokens:
                return None

            # Find the operator with the lowest precedence
            # higher number than all percedence
            min_precedence = 5
            min_index = -1

            for i, token in enumerate(tokens):
                if token in operators and operators[token] < min_precedence:
                    min_precedence = operators[token]
                    min_index = i

            if min_index == -1:
                # it's a terminal node as there is no operator
                # create a node with the variable name and set name
                return Node(tokens[0], tokens[1])

            # not terminal node as an operator was found min_index != -1
            # create a node with just the operator as the value
            # and slice tokens for left and right children
            node = Node(tokens[min_index])
            node.left_child = build_tree(tokens[:min_index])
            node.right_child = build_tree(tokens[min_index + 1:])

            return node

        root = build_tree(tokens)
        
        # create rule and append it to list of rules 
        #! ff @ 15 plz
        frule = Rule(root, rule_out[0], rule_out[1])
        self.rules.append(frule)
        
    def run_simulation(self, crisp_values):
        # fuzzification
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
                #! care for upper()!
                fuzzy_system.add_fuzzy_set(var_name.upper(), set_name.upper(), set_type, set_values)
        
        elif user_input == "3":
            print("Enter the rules in this format: (Press x to finish)")
            print("IN_variable set operator IN_variable set => OUT_variable set")
            rule = input()
            rule = rule.split('=>')
            if rule[0] == "x":
                break
            rule_in = rule[0].upper()
            rule_out = rule[1].upper()
            fuzzy_system.add_rule(rule_in, rule_out)
        elif user_input == "4":
            #todo crisp input and simulation
            print("Enter the crisp values:")
            crisp_values = {}
            for variable in fuzzy_system.variables:
                value = input(f"{variable.name}: ")
                crisp_values[variable.name] = float(value)
            fuzzy_system.run_simulation(crisp_values)
            break


if __name__ == "__main__":
    main()