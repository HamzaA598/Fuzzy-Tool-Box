def test_input_variable():    
    new_variable = input().split()
    variable_name, variable_type, *variable_range = new_variable
    variable_range = eval(variable_range[0] + variable_range[1])
    print(variable_range[0])
    print(variable_range[1])


def test_inference():
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
    
    def inference(self, fuzzy_inputs):
        def parse(in_tree):
            if in_tree.value == "and":
                return min(parse(in_tree.left_child), parse(in_tree.right_child))
            if in_tree.value == "or":
                return max(parse(in_tree.left_child), parse(in_tree.right_child))
        
            # checkpoint
            # return the membership degree of the variable name in set var_set
            return fuzzy_inputs[in_tree.var_name][in_tree.var_set]

        output_membership_degrees = {}
        for rule in self.rules:
            output_membership_degree = parse(rule)
            if rule.out_var not in self.output_membership_degrees:
                output_membership_degree[rule.out_var] = []
            output_membership_degree[rule.out_var].append(output_membership_degree)

        return output_membership_degrees
    
    crisp_values = {}
    for variable in fuzzy_system.variables:
        value = input(f"{variable.name}: ")
        crisp_values[variable.name] = float(value)
    fuzzy_system.run_simulation(crisp_values)
    fuzzy_inputs = fuzzification(crisp_values)
        # inference
    output_membership_degrees = inference(fuzzy_inputs)
        
