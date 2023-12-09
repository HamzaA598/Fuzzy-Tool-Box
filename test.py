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


class Node:
    def __init__(self, value, var_set = None):
        self.value = value
        self.left_child = None
        self.right_child = None
        self.var_set = var_set
    
    
def add_rule(rule_in_str, rule_out_str):
    rule_in_str = rule_in_str.replace('NOT ', '~')
    rule_out = rule_out_str.split()
    tokens = rule_in_str.split()

    # define the operators and their precedence
    # not sure if and is first or or is first
    # currently assumes or is done first (lower in the tree)
    operators = {'AND': 2, 'OR': 1}

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

        # not terminal node as an operator was found
        # create a node with just the operator as the value
        # and slice tokens for left and right children
        node = Node(tokens[min_index])
        node.left_child = build_tree(tokens[:min_index])
        node.right_child = build_tree(tokens[min_index + 1:])

        return node

    root = build_tree(tokens)
    
    frule = Rule(root, rule_out[0], rule_out[1])
    frule.print_rule(root)

#examples:
# proj_funding high or exp_level expert => risk low
# proj_funding very_low and not exp_level expert => risk high
# dirt small and not fabric soft or dirt medium and fabric soft => wash small

inp1 = "proj_funding high or exp_level expert => risk low"
inp2 = "proj_funding very_low and not exp_level expert => risk high"
inp3 = "dirt small and not fabric soft or dirt medium and fabric soft => wash small"

# change inp1 to inp2 to inp3 etc
rule = inp1.split('=>')
rule_in = rule[0].upper()
rule_out = rule[1].upper()
add_rule(rule_in, rule_out)
print("hi")


