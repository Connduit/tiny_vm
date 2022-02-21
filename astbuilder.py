from qklib.grammar import quack_grammar
import quackgen
from lark import Lark, Transformer, v_args, Token, Tree
from os import path
import argparse
import json
from type_checker import TypeChecker


def cli():
    arg_parser = argparse.ArgumentParser(description="Compiles Quack into ASM")
    arg_parser.add_argument("-f", "--filename", required=True, help="Quack Source File")
    return arg_parser


@v_args(tree=True)
class ASTBuilder(Transformer):
    def m_add(self, tree):
        #tree.data = "plus"
        #print(f"tree.children[0] = {tree.children[0]}")
        #print(f"tree.children[1:] = {tree.children[1:]}")
        #print(f"tree.children[1].children = {tree.children[1].children}")
        # tree.children[0] = lit_num
        # tree.children[1:) = # the rest of the tree

        return tree

    def m_sub(self, tree):
        #tree.data = "Int"
        #tree.data = "test"
        #print(f"sub children = {tree.children}")
        # change NAME to Int?
        #tree.children.insert(0, Token("NAME", "minus"))
        return tree

    def m_mul(self, tree):
        #tree.data = "Int"
        #print(f"mul children = {tree.children}")
        # change NAME to Int?
        #tree.data = "test"
        #tree.children.insert(0, Token("NAME", "times"))
        return tree

    def m_div(self, tree):
        #tree.data = "Int"
        #print(f"div children = {tree.children}")
        # change NAME to Int?
        #tree.data = "test"
        #tree.children.insert(0, Token("NAME", "divide"))
        return tree

    # TODO:
    def if_block(self, tree):
        cond, block = tree.children[0], tree.children[1]
        return tree

    # TODO:
    def while_block(self, tree):
        return tree

    def cond_and(self, tree):
        #tree.type = "Bool"
        return tree

    def cond_or(self, tree):
        #tree.type = "Bool"
        return tree

    def cond_not(self, tree):
        #tree.type = "Bool"
        return tree

    def m_equal(self, tree):
        #tree.data = "test"
        #tree.type = "Bool"
        return tree

    def m_notequal(self, tree):
        #tree.type = "Bool"
        #tree.data = "test"
        return tree

    def m_less(self, tree):
        #tree.data = "test"
        #tree.type = "Bool"
        return tree

    def m_more(self, tree):
        #tree.data = "test"
        #tree.type = "Bool"
        return tree

    def m_atmost(self, tree):
        #tree.data = "test"
        #tree.type = "Bool"
        return tree

    def m_atleast(self, tree):
        #tree.data = "test"
        #tree.type = "Bool"
        return tree

    def m_call(self, tree: Tree):
        #print(f"m_call child0 = {tree.children[0]}")
        #print(f"m_call child1 = {tree.children[1]}")
        return tree

    def m_args(self, tree):
        return tree

    def lit_true(self, tree):
        #tree.type = "Bool"
        #tree.children[0].type = "Bool"
        return tree

    def lit_false(self, tree):
        #tree.type = "Bool"
        #tree.children[0].type = "Bool"
        return tree

    def lit_nothing(self, tree):
        #tree.type = "Nothing"
        #tree.children[0].type = "Nothing"
        return tree

    def lit_num(self, tree):
        #TODO: i dont have to declare types here if i do it in type_checker.py
        tree.children[0].type = "Int"
        return tree

    def lit_str(self, tree: Tree):
        #tree.data = "String test"
        tree.type = "String"
        if "\n" in tree.children[0]:
            tree.children[0] = repr(tree.children[0].strip("\"'")).strip("\"'")
        else:
            tree.children[0] = tree.children[0].strip("\"'")
        #tree.children[0].type = "String"
        #tree.type = "String"
        return tree

    def m_neg(self, tree):
        tree.data = "test"
        tree.children.insert(0, Token("NAME", "negate"))
        return tree

    def var(self, tree):
        #print(f"var children = {tree.children}")
        #print(f"var type = {tree.children[0].type}")
        # var_name = tree.children[0].value
        # TODO: find var_value/var_type by looking up var_name in self.variables?

        return tree

    def assignment(self, tree):
        #print(f"children = {tree.children}")
        # len(tree.children) = 3; var_name, var_type, l_op
        return tree


def main():
    # TODO: raw expressions should be immediately popped from the stack as they will never be used
    args = cli()
    sourceFilename = vars(args.parse_args())["filename"]
    if not path.exists(sourceFilename):
        print("Not a valid file or path to file")
        args.print_usage()
        exit()

    quack_parser = Lark(quack_grammar, parser='lalr')
    sourceFile = open(sourceFilename, "r")
    text = sourceFile.read()
    tree = quack_parser.parse(text)
    #print(tree.pretty("    "))
    tree = ASTBuilder().transform(tree)
    #print(tree.pretty("    "))
    #print(tree)

    with open("./qklib/builtin_methods.json", "r") as f:
        types = json.load(f)

    tc = TypeChecker()
    tc.visit(tree)

    g = quackgen.QkGen(types)
    g.visit(tree)
    quackgen.build(sourceFilename, g.instructions, g.variables)
    sourceFile.close()


# TODO: still might need to add negate method for booleans in builtins.c


if __name__ == '__main__':
    main()
