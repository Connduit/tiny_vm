from lark import Lark, Transformer, v_args
import sys

quack_grammar = """
    ?start: program
        
    ?program: line+
    
    ?line: func ";" NEWLINE
        | func NEWLINE
        | assignment ";" NEWLINE
        | assignment NEWLINE
        
    ?assignment: NAME ":" type "=" func -> assign_var
        
    ?type: NAME
        
    ?func: sum
        | func "." NAME "()"        -> func_call
        
    ?sum: product
        | sum "+" product           -> add
        | sum "-" product           -> sub

    ?product: atom
        | product "*" atom          -> mul
        | product "/" atom          -> div

    ?atom: NUMBER                   -> number
        | STRING                    -> string
        | NAME                      -> get_var
        | "-" atom                  -> neg
        | "(" sum ")" 

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE
    %import common.NEWLINE
    %import common.ESCAPED_STRING -> STRING

    %ignore WS_INLINE
"""


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
        try:
            self.instr.append(f"load {var}")
        except KeyError:
            raise Exception("Variable not found: %s" % var)

    def store_var(self, name, value):
        self.vars[name] = value
        self.instr.append(f"store {name}")

    def method(self, op_name, val_type, roll=0):
        if roll:
            self.instr.append("roll 1")

        self.instr.append(f"call {val_type}:{op_name}")

    def build(self, filename):
        output_file = open(f"./tests/src/{filename}.asm", "w")

        output_file.write(f".class {filename}:Obj\n\n")
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
        self.parser = qkParser()
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
        qk_Parser.method("plus", self.types[x], 1)
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
        self.sub(self.const(0), "Int", 1)
        return x

    def assign_var(self, name, var_type, value):
        self.types[name] = var_type
        qk_Parser.store_var(name, value)
        return name

    def get_var(self, name):
        try:
            qk_Parser.load_var(name)
            return qk_Parser.get_var(name)
        except KeyError:
            raise Exception("Variable not found: %s" % name)

    def func_call(self, val, func):
        qk_Parser.method(func, self.types[val])


def main():
    if len(sys.argv) != 2:
        print(f"{sys.argv[0]} takes one .qk file as an argument")
        exit(1)

    sourceFilename = sys.argv[1].split(".")[0]
    sourceFile = open(f"{sourceFilename}.qk", "r")

    parser = Lark(quack_grammar, parser='lalr', transformer=qkTransformer())
    qk = parser.parse
    qk(sourceFile.read())
    sourceFile.close()
    qk_Parser.build(sourceFilename)


if __name__ == '__main__':
    main()
