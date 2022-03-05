from lark import Tree
from lark.visitors import Visitor_Recursive
from copy import deepcopy


class ClassInitializer(Visitor_Recursive):
    def __init__(self, types):
        self.types = types

    def visit(self, tree: Tree):
        super().visit(tree)

    def _class(self, tree: Tree):
        sig, body = tree.children
        name = sig.children[0]
        formal_args = sig.children[1]
        n = len(formal_args.children) // 2
        arg_types = dict([(formal_args.children[ind], formal_args.children[ind+1]) for ind in range(n)])
        super_type = "Obj" if sig.children[2] is None else sig.children[2]

        super_class = self.types[super_type]
        super_methods = deepcopy(super_class["methods"])
        super_fields = deepcopy(super_class["fields"])

        self.types[name] = {
            "super": super_type,
            "methods": super_methods,
            "fields": super_fields
        }

        statements, methods = body.children
        c_method = Tree("method", [
            "$constructor",
            formal_args,
            "Nothing",
            Tree("statement_block", statements.children)
        ])

        c_method.name = "$constructor"
        c_method.arg_types = arg_types
        c_method.ret_type = "Nothing"

        methods.children.insert(0, c_method)
        for method in methods.children:
            self.types[name]["methods"][method.name] = {
                "params": method.arg_types,
                "ret": method.ret_type
            }
        body.children.pop(0)

    def method(self, tree: Tree):
        tree.name = tree.children[0]
        formal_args = tree.children[1]

        n = len(formal_args.children) // 2
        tree.arg_types = dict([(formal_args.children[ind], formal_args.children[ind+1]) for ind in range(n)])
        tree.ret_type = "Nothing" if tree.children[2] is None else tree.children[2]


class FieldInitializer(Visitor_Recursive):
    def __init__(self, types):
        self.types = types
        self.exists = set()
        self.visited = set()
        self.curr_method = ""

    def visit(self, tree: Tree):
        if tree.data == "_class":
            self._class(tree)
        if tree.data == "method":
            self.method(tree)

        if tree.data == "if_block":
            self.if_block(tree)
        elif tree.data == "while_block":
            self.while_block(tree)
        else:
            for child in tree.children:
                if isinstance(child, Tree):
                    self.visit(child)
            self._call_userfunc(tree)
        #super().visit(tree)

    def _class(self, tree: Tree):
        free_fields = self.visited - self.exists
        if free_fields:
            print(f"{free_fields} not defined")
            exit()

        class_name = tree.children[0].children[0]
        fields = self.types[class_name]["fields"]
        for field in self.exists:
            if field not in fields:
                fields[field] = ""

        self.exists = set()
        self.visited = set()

    def method(self, tree: Tree):
        self.curr_method = tree.children[0]

    def if_block(self, tree: Tree):
        pass

    def while_block(self, tree: Tree):
        pass

    def load_field(self, tree: Tree):
        obj, field = tree.children
        if field not in self.exists:
            print(f"field '{field}' is not defined ")
            exit()

    def store_field(self, tree: Tree):
        obj, field, var = tree.children
        self.exists.add(field)
        self.visited.add(field)

