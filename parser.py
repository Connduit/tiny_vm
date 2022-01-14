from lark import Lark, Transformer, v_args

quack_grammar = """
    ?start: sum

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
        | "-" atom          -> neg
        | "(" sum ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):

    def __init__(self):
        self.vars = {}

    def number(self, num):
        return f"\tconst {num}\n"

    def add(self, x, y):
        return f"{x}{y}\tcall Int:plus\n"

    def sub(self, x, y):
        return f"{x}{y}\tcall Int:minus\n"

    def mul(self, x, y):
        return f"{x}{y}\tcall Int:times\n"

    def div(self, x, y):
        return f"{x}{y}\tcall Int:divide\n"

    def neg(self, x):
        return self.sub(self.number(0), x)


calc_parser = Lark(quack_grammar, parser='lalr', transformer=CalculateTree())
calc = calc_parser.parse


def main():
    f = open("./unit_tests/user.asm", "w")
    f.write(".class Sample:Obj\n\n")
    #f.write(".class User:Obj\n\n")
    f.write(".method $constructor\n")
    f.write("\tenter\n")
    s = input('> ')
    f.write(calc(s))

    f.write("\tcall Int:print\n")
    f.write("\tpop\n")
    f.write("\tconst " + r'"\n"' + "\n")
    f.write("\tcall String:print\n")
    f.write("\treturn 0\n")
    f.close()


if __name__ == '__main__':
    main()
