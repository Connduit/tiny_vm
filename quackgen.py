from lark.visitors import Visitor_Recursive
from lark import Tree
from os import path
from collections import Counter


#TODO: make generalized function for const instructions?
class QkGen(Visitor_Recursive):
    def __init__(self, types):
        #super.__init__()
        self.variables = dict()
        self.instructions = list()
        self.types = types
        self.labels = Counter()

    def label(self, prefix):
        num = self.labels[prefix]
        self.labels.update(prefix)
        return f"{prefix}_{num}"

    def m_add(self, tree):
        #self.instructions.append(f"call {type}:{method}")
        #print(len(tree.children))
        #self.m_call(tree)
        self.instructions.append(f"call {tree.type}:plus")
        return tree

    def m_sub(self, tree):
        #print(tree.children)
        self.instructions.append(f"call {tree.type}:minus")
        return tree

    def m_mul(self, tree):
        #print(tree.children)
        self.instructions.append(f"call {tree.type}:times")
        return tree

    def m_div(self, tree):
        #print(tree.children)
        self.instructions.append(f"call {tree.type}:divide")
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
        self.instructions.append(f"call {tree.children[0].type}:{tree.children[1]}")

    def m_args(self, tree):
        return tree

    def lit_true(self, tree):
        self.instructions.append("const true")

    def lit_false(self, tree):
        self.instructions.append("const false")

    def lit_nothing(self, tree):
        self.instructions.append("const nothing")

    def lit_num(self, tree: Tree):
        #print(tree.children[0])
        self.instructions.append(f"const {tree.children[0]}")

    def lit_str(self, tree):
        #print(tree.children[0])
        self.instructions.append(f"const \"{tree.children[0]}\"")

    def m_neg(self, tree):
        return tree

    def var(self, tree: Tree):
        self.instructions.append(f"load {tree.children[0]}")

    def assignment(self, tree):
        var_name = tree.children[0]
        var_type = tree.children[1]
        var_op = tree.children[2]

        self.variables[var_name] = var_type
        self.instructions.append(f"store {var_name}")

    def visit(self, tree):
        #print(f"tree.data = {tree.data}")
        if tree.data == "DO SOMETHING":
            pass
        else:
            super().visit(tree)


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

    output_file.write("const nothing\n")
    output_file.write("return 0")
    output_file.close()
