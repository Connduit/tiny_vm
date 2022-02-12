from grammar import quack_grammar
from lark import Lark, Transformer, v_args, Token
from os import path
import argparse


def cli():
    arg_parser = argparse.ArgumentParser(description="Compiles Quack into ASM")
    arg_parser.add_argument("-f", "--filename", required=True, help="Quack Source File")
    return arg_parser


# TODO: make a subclass from qkParser for every rule in the grammar
class qkParser:
    def __init__(self):
        self.vars = dict()
        self.instr = list()

    def const(self, token):
        self.instr.append(f"const {token}")

    def add_var(self, var_name, var_type):
        self.vars[var_name] = var_type

    def get_var(self, name):
        return self.vars[name]

    def init_vars(self):
        ret = ".local " if self.vars else ""
        ret += ",".join(list(self.vars.keys())) + "\n"
        return ret

    def load_var(self, var):
        self.instr.append(f"load {var}")

    def store_var(self, name, value):
        self.vars[name] = value
        self.instr.append(f"store {name}")

    def method(self, op_name, val_type, roll=False):
        if roll:
            self.instr.append("roll 1")

        self.instr.append(f"call {val_type}:{op_name}")

    def build(self, filename):
        class_name = path.splitext(filename)[0]

        output_file = open(f"./tests/src/{class_name}.asm", "w")
        output_file.write(f".class {class_name}:Obj\n\n")
        output_file.write(".method $constructor\n")
        output_file.write(self.init_vars())
        output_file.write("enter\n")

        for instr in self.instr:
            output_file.write(f"{instr}\n")

        output_file.write("return 0")
        output_file.close()


#qk_Parser = qkParser()


@v_args(tree=True)
class ASTBuilder(Transformer):

    def m_add(self, tree):
        tree.children.insert(0, Token("NAME", "plus"))
        return tree

    def m_sub(self, tree):
        tree.children.insert(0, Token("NAME", "minus"))
        return tree

    def m_mul(self, tree):
        tree.children.insert(0, Token("NAME", "times"))
        return tree

    def m_div(self, tree):
        tree.children.insert(0, Token("NAME", "divide"))
        return tree

    def if_block(self, tree):
        return tree

    def while_block(self, tree):
        return tree

    def cond_and(self, tree):
        return tree

    def cond_or(self, tree):
        return tree

    def cond_not(self, tree):
        return tree

    def m_equals(self, tree):
        return tree

    def m_notequal(self, tree):
        return tree

    def m_less(self, tree):
        return tree

    def m_more(self, tree):
        return tree

    def m_atmost(self, tree):
        return tree

    def m_atleast(self, tree):
        return tree

    def m_call(self, tree):
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
        return tree

    def lit_str(self, tree):
        return tree

    def m_neg(self, tree):
        return tree

    def var(self, tree):
        return tree




def main():
    # TODO: raw expressions should be immediately popped from the stack as they will never be used
    # TODO: add != operator to builtins.c
    args = cli()
    sourceFilename = vars(args.parse_args())["filename"]
    if not path.exists(sourceFilename):
        print("Not a valid file or path to file")
        args.print_usage()
        exit()

    quack_parser = Lark(quack_grammar, parser='lalr')
    #quack_parser = Lark(quack_grammar)
    sourceFile = open(sourceFilename, "r")
    text = sourceFile.read()
    tree = quack_parser.parse(text)
    print(tree.pretty("    "))
    tree = ASTBuilder().transform(tree)
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


if __name__ == '__main__':
    main()
