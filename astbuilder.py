from qklib.grammar import quack_grammar
from lark import Lark, Transformer, v_args, Token, Tree
from os import path
import argparse


def cli():
    arg_parser = argparse.ArgumentParser(description="Compiles Quack into ASM")
    arg_parser.add_argument("-f", "--filename", required=True, help="Quack Source File")
    return arg_parser


@v_args(tree=True)
class ASTBuilder(Transformer):
    def m_add(self, tree):
        #tree.data = "test"
        tree.children.insert(0, Token("NAME", "plus"))
        return tree

    def m_sub(self, tree):
        #tree.data = "test"
        tree.children.insert(0, Token("NAME", "minus"))
        return tree

    def m_mul(self, tree):
        #tree.data = "test"
        tree.children.insert(0, Token("NAME", "times"))
        return tree

    def m_div(self, tree):
        #tree.data = "test"
        tree.children.insert(0, Token("NAME", "divide"))
        return tree

    # TODO:
    def if_block(self, tree):
        cond, block = tree.children[0], tree.children[1]
        return tree

    # TODO:
    def while_block(self, tree):
        return tree

    def cond_and(self, tree):
        return tree

    def cond_or(self, tree):
        return tree

    def cond_not(self, tree):
        return tree

    def m_equal(self, tree):
        #tree.data = "test"
        return tree

    def m_notequal(self, tree):
        return tree

    def m_less(self, tree):
        #tree.data = "test"
        return tree

    def m_more(self, tree):
        #tree.data = "test"
        return tree

    def m_atmost(self, tree):
        #tree.data = "test"
        return tree

    def m_atleast(self, tree):
        #tree.data = "test"
        return tree

    def m_call(self, tree):
        print(f"m_call children = {tree.children}")
        #tree.children[0], tree.children[1] = tree.children[1], tree.children[0]
        return tree

    def m_args(self, tree):
        return tree

    def lit_true(self, tree):
        return tree

    def lit_false(self, tree):
        return tree

    def lit_none(self, tree):
        return tree

    def lit_num(self, tree):
        #tree.data = "lit_num"
        return tree

    def lit_str(self, tree: Tree):
        #tree.data = "lit_str"
        tree.children[0] = tree.children[0].strip("\"'")
        return tree

    def m_neg(self, tree):
        return tree

    def var(self, tree):
        return tree

    def assignment(self, tree):
        #print(f"children = {tree.children}")
        # len(tree.children) = 3; var_name, var_type, l_op
        return tree

    def inf_assignment(self, tree):
        # len(tree.children) = 2; var_name, l_op
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
    print(tree.pretty("    "))
    tree = ASTBuilder().transform(tree)
    #print(tree.pretty("    "))
    print(tree)
    sourceFile.close()

    """
    sourceFile = open(sourceFilename, "r")
    parser = Lark(quack_grammar, parser='lalr', transformer=qkTransformer())
    qk = parser.parse
    qk(sourceFile.read())
    sourceFile.close()
    qk_Parser.build(sourceFilename)
    """

# TODO: still might need to add negate method for booleans in builtins.c


if __name__ == '__main__':
    main()
