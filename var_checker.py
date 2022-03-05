from lark.visitors import Visitor_Recursive
from lark import Tree
import json


class VarChecker(Visitor_Recursive):
    def __init__(self):
        # changed to self.variables = {"this"} ?
        self.variables = set()
        self.constructor = False
        self.fields = set()
        self.fields_visited = set()

    def visit(self, tree):
        #print(tree.data)
        if tree.data == "store_field":
            self.store_field(tree)
        elif tree.data == "typecase":
            self.typecase(tree)
        elif tree.data == "_class":
            #TODO: reset vars/fields or just fields?
            """
            self.variables = set()
            self.constructor = True  # ?
            self.class_fields = set()
            self.class_fields_seen = set()
            """
            super().visit(tree)
        else:
            super().visit(tree)

    def typecase(self, tree: Tree):
        pass

    def store_field(self, tree: Tree):
        if self.constructor:
            self.fields.add(tree.children[0])
        self.fields_visited.add(tree.children[0])

    def load_field(self, tree: Tree):
        if self.constructor:
            pass
            #self.class_fields.add()
        pass

    def var(self, tree):
        if tree.children[0] not in self.variables:
            # change print to write to stderror
            print(f"NameError: name '{tree.children[0]}' is not defined")
            exit()

    def method(self, tree):
        self.constructor = True if tree.children[0] == "$constructor" else False
        self.variables = {"this"}

    def assignment(self, tree):
        var_name = tree.children[0]
        self.variables.add(var_name)

    def if_block(self, tree):
        pass

    def while_block(self, tree):
        pass


