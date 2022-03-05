from lark.visitors import Visitor_Recursive
from lark import Tree
import json


class TypeChecker(Visitor_Recursive):
    def __init__(self):
        with open("./qklib/builtin_methods.json", "r") as f:
            self.types = json.load(f)
        self.variables = dict()
        self.class_name = ""
        self.constructor = False

    def visit(self, tree: Tree):
        changed = False
        if not isinstance(tree, Tree):
            return changed

        if tree.data == "_class":
            self._class(tree)
        elif tree.data == "method":
            self.method(tree)
        elif tree.data == "assignment":
            self.assignment(tree)

        for child in tree.children:
            changed = self.visit(child) or changed

        return changed or self._call_userfunc(tree)

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

    def cond_or(self, tree):
        if not (tree.children[0].type == tree.children[1].type == "Bool"):
            print(f"cond_or needs type 'Bool' but {tree.children[0].data} has type '{tree.children[0].type}'")
            print(f"cond_or needs type 'Bool' but {tree.children[1].data} has type '{tree.children[0].type}'")
            exit()

    def cond_not(self, tree):
        if tree.children[0].type != "Bool":
            print(f"cond_not needs type 'Bool' but {tree.children[0].data} has type '{tree.children[0].type}'")
            exit()

    def if_block(self, tree):
        pass

    def while_block(self, tree):
        pass

    def m_call(self, tree):
        item = tree.children[0].children[0]
        m_name = tree.children[1]
        try:
            tree.type = self.variables[item]
        except KeyError:
            tree.type = tree.children[0].type

    def var(self, tree):
        try:
            tree.type = self.variables[tree.children[0]]
        except KeyError:
            print(f"cannot find type for undefined variable {tree.children[0]}")
            exit()

    def assignment(self, tree):
        if tree.children[1] is not None:
            var_type = tree.children[1]
        else:
            var_type = tree.children[2].type

        var_name = tree.children[0]
        var_value = tree.children[2]

        old_type = self.variables.get(var_name, "")
        shared_type = self.shared_ancestor(old_type, var_type)

        tree.type = shared_type
        self.variables[var_name] = shared_type

    #TODO
    def load_field(self, tree: Tree):
        obj, field = tree.children
        try:
            field_type = self.types[obj.type]["fields"][field]
        except KeyError:
            print('bad load')
            exit()

    #TODO
    def store_field(self, tree: Tree):
        obj, field, value = tree.children
        try:
            field_type = self.types[obj.type]['fields'][field]
        except KeyError:
            print('bad store')
            exit()

        #TODO: obj.type should return the class that owns it
        this_obj = obj.type in self.types and obj == "this"
        if self.constructor and this_obj:
            if field.type == "IDENT":
                field_type = None
            else:
                field_type = field.type
            new_type = self.shared_ancestor(value.type, field_type)
            try:
                #TODO: fix obj.type
                self.types[obj.type]['fields'][field] = new_type
                tree.type = new_type
            except KeyError:
                print("key error")
                exit()

    def _class(self, tree: Tree):
        self.class_name = tree.children[0].children[0]

    def method(self, tree: Tree):
        self.constructor = True if tree.children[0] == "$constructor" else False

        try:
            self.variables = tree.vars
        except AttributeError:
            self.variables = {"this": self.class_name}
            tree.vars = self.variables

        for ind in range(0, len(tree.children[1].children), 2):
            var_name = tree.children[1].children[ind]
            var_type = tree.children[1].children[ind+1]
            self.variables[var_name] = var_type

    def shared_ancestor(self, obj1, obj2):
        if not obj1 and obj2:
            return obj2
        elif not obj2 and obj1:
            return obj1
        elif obj1 == obj2:
            return obj1
