from lark import Lark, Transformer, v_args
from os import path
import argparse


def cli():
    arg_parser = argparse.ArgumentParser(description="Compiles Quack into ASM")
    arg_parser.add_argument("-f", "--filename", required=True, help="Quack Source File")
    #args = arg_parser.parse_args()
    return arg_parser


quack_grammar = """
    ?start: program
        
    ?program: line*
    
    ?line: func ";" 
        | assignment ";" 
        
    ?assignment: NAME ":" type "=" func -> assign_var
    
    ?type: NAME
        
    ?func: sum
        | sum "." NAME "()"        -> func_call
        
    ?sum: product
        | sum "+" product           -> add
        | sum "-" product           -> sub

    ?product: atom
        | product "*" atom          -> mul
        | product "/" atom          -> div

    ?atom: NUMBER                   -> number
        | NAME                      -> var
        | STRING                    -> string
        | "-" atom                  -> neg
        | "(" sum ")" 
        | "true"                    -> lit_true
        | "false"                   -> lit_false
        | "none"                    -> lit_nothing
        
    
    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE
    %import common.NEWLINE
    %import common.ESCAPED_STRING -> STRING
    
    COMMENT: "//" /[^\n]*/x
        | "/*" /(.)*/xs "*/"

    %ignore WS_INLINE
    %ignore NEWLINE
    %ignore COMMENT
"""


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


qk_Parser = qkParser()


@v_args(inline=True)    # Affects the signatures of the methods
class qkTransformer(Transformer):

    def __init__(self):
        self.types = dict()

    def number(self, token):
        self.types[token] = "Int"
        qk_Parser.const(token)
        return token

    def string(self, token):
        self.types[token] = "String"
        qk_Parser.const(token)
        return token

    def add(self, x, y):
        roll = True if self.types[x] == "String" else False
        qk_Parser.method("plus", self.types[x], roll)
        return x

    def sub(self, x, y):
        qk_Parser.method("minus", self.types[x], 1)
        return x

    def mul(self, x, y):
        qk_Parser.method("times", self.types[x])
        return x

    def div(self, x, y):
        qk_Parser.method("divide", self.types[x], 1)
        return x

    def neg(self, x):
        qk_Parser.method("negate", self.types[x])
        return x

    def assign_var(self, name, var_type, value):
        self.types[name] = var_type
        qk_Parser.store_var(name, value)
        return name

    def var(self, name):
        try:
            qk_Parser.load_var(name)
            return qk_Parser.get_var(name)
        except KeyError:
            raise Exception("Variable not found: %s" % name)

    def func_call(self, val, func):
        qk_Parser.method(func, self.types[val])
        return val

    def lit_true(self):
        self.types["true"] = "Bool"
        qk_Parser.const("true")
        return "true"

    def lit_false(self):
        self.types["false"] = "Bool"
        qk_Parser.const("false")
        return "false"

    def lit_nothing(self):
        self.types["none"] = "Nothing"
        qk_Parser.const("none")
        return "none"


def main():
    args = cli()
    sourceFilename = vars(args.parse_args())["filename"]
    if not path.exists(sourceFilename):
        print("Not a valid file or path to file")
        args.print_usage()
        exit()

    sourceFile = open(sourceFilename, "r")
    parser = Lark(quack_grammar, parser='lalr', transformer=qkTransformer())
    qk = parser.parse
    qk(sourceFile.read())
    sourceFile.close()
    qk_Parser.build(sourceFilename)


if __name__ == '__main__':
    main()
