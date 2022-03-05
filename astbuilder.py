from lark import Transformer, v_args, Token, Tree


@v_args(tree=True)
class ASTBuilder(Transformer):
    def __init__(self, default_classname="Main"):
        self.default_classname = default_classname

    def m_add(self, tree):
        tree.type = ""
        return tree

    def m_sub(self, tree):
        tree.type = ""
        return tree

    def m_mul(self, tree):
        tree.type = ""
        return tree

    def m_div(self, tree):
        tree.type = ""
        return tree

    def if_block(self, tree):
        tree.type = ""
        return tree

    def while_block(self, tree):
        tree.type = ""
        return tree

    def cond_and(self, tree):
        tree.type = "Bool"
        return tree

    def cond_or(self, tree):
        tree.type = "Bool"
        return tree

    def cond_not(self, tree):
        tree.type = "Bool"
        return tree

    def m_equal(self, tree):
        tree.type = "Bool"
        return tree

    def m_notequal(self, tree):
        tree.type = "Bool"
        return tree

    def m_less(self, tree):
        tree.type = "Bool"
        return tree

    def m_more(self, tree):
        tree.type = "Bool"
        return tree

    def m_atmost(self, tree):
        tree.type = "Bool"
        return tree

    def m_atleast(self, tree):
        tree.type = "Bool"
        return tree

    def m_call(self, tree: Tree):
        tree.type = ""
        return tree

    def m_args(self, tree):
        tree.type = ""
        return tree

    def lit_true(self, tree):
        tree.type = "Bool"
        return tree

    def lit_false(self, tree):
        tree.type = "Bool"
        return tree

    def lit_nothing(self, tree):
        tree.type = "Nothing"
        return tree

    def lit_num(self, tree):
        tree.children[0].type = "Int"
        tree.type = "Int"
        return tree

    def lit_str(self, tree: Tree):
        tree.type = "String"
        if "\n" in tree.children[0]:
            tree.children[0] = repr(tree.children[0].strip("\"'")).strip("\"'")
        else:
            tree.children[0] = tree.children[0].strip("\"'")
        #tree.children[0].type = "String"
        #tree.type = "String"
        return tree

    def m_neg(self, tree):
        # Int:negate
        tree.type = ""
        tree.children.insert(0, Token("IDENT", "negate"))
        return tree

    def var(self, tree):
        tree.type = ""
        return tree

    def assignment(self, tree):
        #print(f"children = {tree.children}")
        tree.type = ""
        return tree

    def program(self, tree: Tree):
        classes = list()
        statements = list()
        for child in tree.children:
            if isinstance(child, Tree):
                # child doesn't belong to a class
                statements.append(child)
            else:
                classes.append(child)

        new_tree = Tree("_class", [
            Tree("class_sig", [
                self.default_classname,
                Tree("formal_args", []),
                "Obj"
            ]),
            Tree("class_body", [
                Tree(Token("RULE", "statements"), []),
                Tree("methods", [
                    Tree("method", [
                        "$constructor",
                        Tree("formal_args", []),
                        "Nothing",
                        Tree("statement_block", statements)
                    ])
                ])
            ])
        ])
        classes.append(new_tree)
        tree.children = classes
        return tree

    def _class(self, tree):
        #class: class_sig class_body -> _class
        new_tree = Tree("_class", [tree[0], tree[1]])
        return new_tree

    def class_sig(self, tree: Tree):
        #class_sig: "class" IDENT "(" formal_args ")" [ "extends" IDENT ] -> class_sig
        tree.type = ""
        return tree

    def formal_args(self, tree: Tree):
        #?formal_args: [IDENT ":" IDENT ("," IDENT ":" IDENT)* ] -> formal_args
        tree.type = ""
        return tree

    def class_body(self, tree):
        #?class_body: "{" statement* method* "}" -> class_body
        tree.type = ""
        return tree

    def method(self, tree):
        method_name = tree.children[0]
        formal_args = tree.children[1]
        tree.type = method_name
        return tree

    def statement_block(self, tree: Tree):
        tree.type = ""
        return tree

    def c_call(self, tree):
        tree.type = ""
        return tree

    #TODO: change type of obj token
    def store_field(self, tree: Tree):
        tree.type = ""
        lhs, rhs = tree.children
        obj, field = lhs.children
        return Tree("store_field", [obj, field, rhs])

    #TODO: change type of obj token
    def load_field(self, tree: Tree):
        tree.type = ""
        obj = tree.children[0].children[0]
        field = tree.children[1]
        return Tree("load_field", [obj, field])

