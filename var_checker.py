from lark.visitors import Visitor_Recursive
from lark import Tree
import json


class VarChecker(Visitor_Recursive):
    def __init__(self):
        self.variables = set()

    def visit(self, tree):
        super().visit(tree)

    def var(self, tree):
        if tree.children[0] not in self.variables:
            print(f"Variable {tree.children[0]} is undefined")
            exit()

    def inf_assignment(self, tree):
        var_name = tree.children[0]
        #var_value = tree.children[1]
        self.variables.add(var_name)

    def assignment(self, tree):
        var_name = tree.children[0]
        #var_type = tree.children[1]
        #var_value = tree.children[2]
        self.variables.add(var_name)

    def if_block(self, tree):
        pass

    def while_block(self, tree):
        pass


