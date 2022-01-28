from lark import Lark, Transformer, v_args
import sys

quack_grammar = """
    ?start: sum
        | NAME ":" NAME "=" sum -> assign_var
        
    ?sum: product
        | sum "+" product           -> add
        | sum "-" product           -> sub

    ?product: atom
        | product "*" atom          -> mul
        | product "/" atom          -> div

    ?atom: NUMBER                   -> number
        | "-" atom                  -> neg
        | NAME                      -> var
        | NAME /\.([a-z])\w+\(\)(;)?/   -> print_var
        | "(" sum ")" 
        | NUMBER ";"                -> number
    

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):

    def __init__(self, file):
        #TODO: add var_type and var_value to self.vars?
        self.vars = {}
        self.file = file

    def number(self, num):
        return f"""
        const {num}
        """

    def print_var(self, name, method):
        ind = method.index("(")
        m = method[1:ind]
        return f"""
        load $
        load_field $:{name}
        call {self.vars[name]}:{m}
        pop
        """

    #def add(self, x, y, var_type):
    def add(self, x, y):
        return f"{x}{y}call Int:plus\n"

    def sub(self, x, y):
        return f"{x}{y}call Int:minus\n"

    def mul(self, x, y):
        return f"{x}{y}call Int:times\n"

    def div(self, x, y):
        return f"{x}{y}call Int:divide\n"

    def neg(self, x):
        return self.sub(self.number(0), x)

    def assign_var(self, name, var_type, value):
        self.file.write(f".field {name}\n")
        self.vars[name] = var_type
        return f"""
        {value}
        load $
        store_field $:{name}"""

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)


def main():

    sourceFilename = sys.argv[1].split(".")[0]
    sourceFile = open(f"{sourceFilename}.qk", "r")

    asmFile = open(f"./tests/src/{sourceFilename}.asm", "w")
    calc_parser = Lark(quack_grammar, parser='lalr', transformer=CalculateTree(asmFile))
    calc = calc_parser.parse

    asmFile.write(f".class {sourceFilename}:Obj\n")
    print(f".class {sourceFilename}:Obj")

    line = sourceFile.readline().strip()
    list_of_asm_lines = list()
    while line:
        temp = calc(line)
        print(temp)
        #asmFile.write(temp)
        list_of_asm_lines.append(temp)
        line = sourceFile.readline().strip()

    asmFile.write(f".method $constructor\n")
    asmFile.write(f"enter\n")
    for i in list_of_asm_lines:
        asmFile.write(i)

    print("\tconst nothing")
    print("\treturn 0")

    asmFile.write("const nothing\n")
    asmFile.write("return 0\n")
    asmFile.close()


if __name__ == '__main__':
    main()
