new_variable = input().split()
variable_name, variable_type, *variable_range = new_variable
variable_range = eval(variable_range[0] + variable_range[1])
print(variable_range[0])
print(variable_range[1])