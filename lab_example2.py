# node class for rules' tree
class Node:
    def __init__(self, value, var_set = None):
        self.value = value
        self.left_child = None
        self.right_child = None
        # the set of the variable in the inference rule
        self.var_set = var_set

class variable:
    def __init__(self, name, type, v_range):
        self.name = name
        self.type = 0 if type.upper() == "IN" else 1
        self.range = v_range
        # need it to be a set when defuzzifying
        # in order to retrieve the centroid of a specific set
        self.sets = {}
        
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
        # contains all variables
        self.variables = {}
        # only contains output variable
        self.output_variable = None
        self.rules = []
        
    def add_variable(self, variable_name, variable_type, variable_range):
        new_variable = variable(variable_name, variable_type, variable_range)
        self.variables[variable_name] = new_variable
        if new_variable.type == 1:
            self.output_variable = new_variable
    
    def add_fuzzy_set(self, var_name, set_name, set_type, set_values):
        var = self.variables[var_name]
        for value in set_values:
            if value < var.range[0] or value > var.range[1]:
                #todo SHOW ERROR SOMEHOW
                pass
        fset = Set(set_name, set_type, set_values)
        var.sets[set_name] = fset
    
    #! is this correct????????????????
    #! not sure if overcomplicating or not
    #! add_rule function creates a syntax tree for the rule evaluation
    #! check test.py for testing the rule creation with examples
    def add_rule(self, rule_in_str, rule_out_str):
        rule_in_str = rule_in_str.replace('not ', '~')
        rule_out = rule_out_str.split()
        tokens = rule_in_str.split()

        # define the operators and their precedence
        # not sure if and is first or or is first
        # currently assumes or is done first (lower in the tree)
        operators = {'and': 2, 'or': 1}

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
    
    @staticmethod
    def fuzzify_variable(var, value):
        membership_values = {}
        for fuzzy_set in var.sets.values():
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
    
    def fuzzification(self, crisp_values):
        fuzzy_inputs = {}
        for var_name, value in crisp_values.items():
            var = self.variables[var_name]
            if var.type == 1:
                continue # don't need to fuzzify out variables i think?
            fuzzy_inputs[var_name] = FuzzySystem.fuzzify_variable(var, value)
        return fuzzy_inputs
    
    def inference(self, fuzzy_inputs):
        # it is a rule not a node
        def parse(in_tree):
            if in_tree.value[0] == "~":
                return 1-fuzzy_inputs[in_tree.value[1:]][in_tree.var_set]
            if in_tree.value == "and":
                return min(parse(in_tree.left_child), parse(in_tree.right_child))
            if in_tree.value == "or":
                return max(parse(in_tree.left_child), parse(in_tree.right_child))

            # handle: test
            # return the membership degree of the variable name in set var_set
            return fuzzy_inputs[in_tree.value][in_tree.var_set]

        output_membership_degrees = {}
        for rule in self.rules:
            output_membership_degree = parse(rule.in_tree)
            if rule.out_var not in output_membership_degrees:
                output_membership_degrees[rule.out_var] = {}
            if rule.out_set not in output_membership_degrees[rule.out_var]:
                output_membership_degrees[rule.out_var][rule.out_set] = []
            output_membership_degrees[rule.out_var][rule.out_set].append(output_membership_degree)

        return output_membership_degrees
    
    def defuzzification(self, output_membership_degrees):
        total, weights = 0, 0
        for out_var in output_membership_degrees:
            for var_set in output_membership_degrees[out_var]:
                for membership_degree in output_membership_degrees[out_var][var_set]:
                    print(self.variables[out_var].sets)
                    total += (self.variables[out_var].sets)[var_set].center * membership_degree
                    weights += membership_degree
        
        z = total / weights

        # get the set with the maximum membership
        membership_values = self.fuzzify_variable(self.output_variable, z)
        max_membership_degree, output_set = -1, ""
        for current_set, membership_degree in membership_values.items():
            if membership_degree > max_membership_degree:
                max_membership_degree = membership_degree
                output_set = current_set
        return output_set, z
    
    def run_simulation(self, crisp_values):
        # fuzzification
        fuzzy_inputs = self.fuzzification(crisp_values)
        # inference
        output_membership_degrees = self.inference(fuzzy_inputs)
        # defuzzification
        output_set, z = self.defuzzification(output_membership_degrees)

        return output_set, z
    
fuzzy_system = FuzzySystem("Example System", "Testing fuzzy system")

fuzzy_system.add_variable('Dirt', 'IN', (0, 100))
fuzzy_system.add_variable('Fabric', 'IN', (0, 100))
fuzzy_system.add_variable('Wash', 'OUT', (0, 60))

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