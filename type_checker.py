from lark.visitors import Visitor_Recursive
from lark import Tree
import json


class TypeChecker(Visitor_Recursive):
    def __init__(self):
        with open("./qklib/builtin_methods.json", "r") as f:
            self.types = json.load(f)
        self.variables = dict()
        self.changed = False

    def visit(self, tree):
        changed = False
        if not isinstance(tree, Tree):
            return changed

        #print(tree.data)
        for child in tree.children:
            changed = self.visit(child) or changed

        ret = self._call_userfunc(tree)
        return changed or ret

    def m_add(self, tree):
        item_type = tree.children[0].children[0].type
        try:
            method = self.types[item_type]
            tree.type = method["methods"]["plus"]["ret"]
        except KeyError:
            tree.type = self.variables[tree.children[0].children[0].value]


    def m_sub(self, tree):
        item_type = tree.children[0].children[0].type
        try:
            method = self.types[item_type]
            tree.type = method["methods"]["minus"]["ret"]
        except KeyError:
            tree.type = self.variables[tree.children[0].children[0].value]


    def m_mul(self, tree):
        item_type = tree.children[0].children[0].type
        try:
            method = self.types[item_type]
            tree.type = method["methods"]["times"]["ret"]
        except KeyError:
            tree.type = self.variables[tree.children[0].children[0].value]


    def m_div(self, tree):
        item_type = tree.children[0].children[0].type
        try:
            method = self.types[item_type]
            tree.type = method["methods"]["divide"]["ret"]
        except KeyError:
            tree.type = self.variables[tree.children[0].children[0].value]


    def lit_str(self, tree):
        pass

    def m_call(self, tree):
        #print(tree.children[0])
        item = tree.children[0].children[0]
        m_name = tree.children[1]
        #new_type = self.shared_ancestor(old_type, var_type)
        try:
            tree.type = self.variables[item]
        except KeyError:
            tree.type = tree.children[0].type

    def var(self, tree):
        #print(tree.children[0].value)
        tree.type = self.variables[tree.children[0]]

    def assignment(self, tree):
        try:
            orig = tree.type
            #var_name = tree.children[0]
        except AttributeError:
            orig = ""

        var_name = tree.children[0]
        var_type = tree.children[1]
        var_value = tree.children[2]
        try:
            imp_type = tree.children[2].type
        except AttributeError:
            imp_type = ""

        old_type = self.variables.get(var_name, "")
        shared_type = self.shared_ancestor(old_type, var_type)
        tree.type = shared_type
        self.variables[var_name] = shared_type

    def get_type(self, tree):
        try:
            return tree.type
        except AttributeError:
            return ""

    def __default__(self, tree):
        try:
            orig = tree.type
        except AttributeError:
            tree.type = ""
        #print(tree.children)

    def shared_ancestor(self, obj1, obj2):
        if not obj1 and obj2:
            return obj2
        elif not obj2 and obj1:
            return obj1
        elif obj1 == obj2:
            return obj1
