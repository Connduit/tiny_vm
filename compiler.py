from qklib.grammar import quack_grammar
import quackgen
from lark import Lark
from os import path
import argparse
import json
from type_checker import TypeChecker
from astbuilder import ASTBuilder
from var_checker import VarChecker
from initializer import ClassInitializer, FieldInitializer


def cli():
    arg_parser = argparse.ArgumentParser(description="Compiles Quack into tinyVM")
    arg_parser.add_argument("-f", "--filename", required=True, help="Quack Source File")
    arg_parser.add_argument("-v", "--visual", action="store_true", help="Print AST to CLI")
    return arg_parser


def main():
    args = cli()
    sourceFilename = vars(args.parse_args())["filename"]
    print_ast = vars(args.parse_args())["visual"]
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

    if print_ast:
        print(tree.pretty("    "))
    #print(tree)

    with open("./qklib/builtin_methods.json", "r") as f:
        types = json.load(f)

    ClassInitializer(types).visit(tree)
    FieldInitializer(types).visit(tree)
    VarChecker().visit(tree)
    TypeChecker().visit(tree)

    g = quackgen.QkGen(types)
    g.visit(tree)
    quackgen.build(sourceFilename, g.instructions, g.variables)

    sourceFile.close()


if __name__ == '__main__':
    main()
