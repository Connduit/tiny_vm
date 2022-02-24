from lark.visitors import Visitor_Recursive
from lark import Tree
import json


class TypeChecker(Visitor_Recursive):
    def __init__(self):
        with open("./qklib/builtin_methods.json", "r") as f:
            self.types = json.load(f)
        self.variables = dict()
        #self.changed = False

    def visit(self, tree):
        changed = False
        if not isinstance(tree, Tree):
            return changed

        for child in tree.children:
            changed = self.visit(child) or changed

        return changed or self._call_userfunc(tree)

    def lit_true(self, tree):
        tree.type = "Bool"

    def lit_false(self, tree):
        tree.type = "Bool"

    def lit_nothing(self, tree):
        tree.type = "Nothing"

    def lit_num(self, tree):
        tree.type = "Int"

    def lit_str(self, tree: Tree):
        tree.type = "String"

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

    def cond_and(self, tree):
        if not (tree.children[0].type == tree.children[1].type == "Bool"):
            print(f"cond_and needs type 'Bool' but {tree.children[0].data} has type '{tree.children[0].type}'")
            print(f"cond_and needs type 'Bool' but {tree.children[1].data} has type '{tree.children[0].type}'")
            exit()

        tree.type = "Bool"

    def cond_or(self, tree):
        if not (tree.children[0].type == tree.children[1].type == "Bool"):
            print(f"cond_or needs type 'Bool' but {tree.children[0].data} has type '{tree.children[0].type}'")
            print(f"cond_or needs type 'Bool' but {tree.children[1].data} has type '{tree.children[0].type}'")
            exit()

        tree.type = "Bool"

    def cond_not(self, tree):
        if tree.children[0].type != "Bool":
            print(f"cond_not needs type 'Bool' but {tree.children[0].data} has type '{tree.children[0].type}'")
            exit()

        tree.type = "Bool"

    def m_equal(self, tree):
        tree.type = "Bool"
        pass

    def m_notequal(self, tree):
        tree.type = "Bool"

    def m_less(self, tree):
        tree.type = "Bool"

    def m_more(self, tree):
        tree.type = "Bool"

    def m_atmost(self, tree):
        tree.type = "Bool"

    def m_atleast(self, tree):
        tree.type = "Bool"

    def if_block(self, tree):
        tree.type = "Bool"

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
        try:
            tree.type = self.variables[tree.children[0]]
        except KeyError:
            tree.type = "unknown"
            print(f"unknown type from {tree.children[0]}")
            #exit()

    def inf_assignment(self, tree):
        try:
            #orig = tree.type
            orig = tree.children[1].type
            #var_name = tree.children[0]
        except AttributeError:
            orig = ""
        var_name = tree.children[0]
        var_value = tree.children[1]
        old_type = self.variables.get(var_name, "")
        new_type = self.shared_ancestor(old_type, orig)
        tree.type = new_type
        self.variables[var_name] = new_type

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

    def __default__(self, tree):
        pass

    def shared_ancestor(self, obj1, obj2):
        if not obj1 and obj2:
            return obj2
        elif not obj2 and obj1:
            return obj1
        elif obj1 == obj2:
            return obj1
        else:
            pass
