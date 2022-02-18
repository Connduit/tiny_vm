from lark import Visitor_Recursive
from lark import Tree
from os import path

#TODO: make generalized function for const instructions
class QkGen(Visitor_Recursive):
    def __init__(self):
        super.__init__()
        self.variables = dict()
        self.instructions = list()

    def m_add(self, tree):
        return tree

    def m_sub(self, tree):
        return tree

    def m_mul(self, tree):
        return tree

    def m_div(self, tree):
        return tree

    # TODO:
    def if_block(self, tree):
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
        self.instructions.append("const true")

    def lit_false(self, tree):
        self.instructions.append("const false")

    def lit_none(self, tree):
        self.instructions.append("const none")

    def lit_num(self, tree: Tree):
        print(tree.children[0])
        self.instructions.append(f"const {tree.children[0]}")

    def lit_str(self, tree):
        print(tree.children[0])
        self.instructions.append(f"const {tree.children[0]}")

    def m_neg(self, tree):
        return tree

    def var(self, tree: Tree):
        self.instructions.append(f"load {tree.children[0]}")

    def assignment(self, tree):
        return tree

    def inf_assignment(self, tree):
        return tree


def build(filename, instructions, variables):

    class_name = path.splitext(filename)[0]

    output_file = open(f"./tests/src/{class_name}.asm", "w")
    output_file.write(f".class {class_name}:Obj\n\n")
    output_file.write(".method $constructor\n")

    if variables:
        output_file.write(f".local {','.join(list(variables.keys()))}\n")

    output_file.write("enter\n")

    for instruction in instructions:
        output_file.write(f"{instruction}\n")

    #output_file.write("const nothing\n")
    output_file.write("const none\n")
    output_file.write("return 0")
    output_file.close()
