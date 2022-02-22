from lark.visitors import Visitor_Recursive
from lark import Tree
from os import path


#TODO: make generalized function for const instructions?
class QkGen(Visitor_Recursive):
    def __init__(self, types):
        #super.__init__()
        self.variables = dict()
        self.instructions = list()
        self.types = types
        self.labels = dict()

    def label(self, prefix):
        num = self.labels.get(prefix, 0) + 1
        self.labels[prefix] = num
        return f"{prefix}_{num}"

    def m_add(self, tree):
        #self.instructions.append(f"call {type}:{method}")
        #print(len(tree.children))
        #self.m_call(tree)
        self.instructions.append(f"call {tree.type}:plus")
        return tree

    def m_sub(self, tree):
        #print(tree.children)
        self.instructions.append(f"roll 1")
        self.instructions.append(f"call {tree.type}:minus")
        return tree

    def m_mul(self, tree):
        #print(tree.children)
        self.instructions.append(f"call {tree.type}:times")
        return tree

    def m_div(self, tree):
        #print(tree.children)
        self.instructions.append(f"roll 1")
        self.instructions.append(f"call {tree.type}:divide")
        return tree

    def if_block(self, tree):
        #print(len(tree.children))
        else_block = tree.children.pop()
        elif_blocks = tree.children[2:]
        if_cond = tree.children[0]
        if_cond_true = tree.children[1]
        #print(if_cond)
        #print(if_cond_true)
        #print(elif_blocks)
        #print(else_block)

        if_label = self.label("if_label")
        else_label = self.label("else_label")
        endif = self.label("endif_label")

        if not elif_blocks and else_block is None:
            self.visit(if_cond)
            self.instructions.append(f"jump_ifnot {endif}")
            self.visit(if_cond_true)
            self.instructions.append(f"jump {endif}")
            self.instructions.append(f"{endif}:")
        elif not elif_blocks and else_block:
            self.visit(if_cond)
            self.instructions.append(f"jump_ifnot {else_label}")
            self.visit(if_cond_true)
            self.instructions.append(f"jump {endif}")
            self.instructions.append(f"{else_label}:")
            self.visit(else_block)
            #self.instructions.append(f"jump {endif}")
            self.instructions.append(f"{endif}:")
        elif elif_blocks and else_block is None:
            conds = len(elif_blocks) // 2
            elif_labels = [self.label("elif_label") for cond in range(conds)]
            self.visit(if_cond)
            self.instructions.append(f"jump_ifnot {elif_labels[0]}")
            self.visit(if_cond_true)
            self.instructions.append(f"jump {endif}")

            for ind in range(conds):
                self.instructions.append(f"{elif_labels[ind]}:")
                self.visit(elif_blocks[ind])
                if ind < conds-1:
                    self.instructions.append(f"jump_ifnot {elif_labels[ind+1]}")
                    self.visit(elif_blocks[ind + 1])
                    self.instructions.append(f"jump {endif}")

            self.instructions.append(f"{endif}:")
        elif elif_blocks and else_block:
            conds = len(elif_blocks) // 2
            elif_labels = [self.label("elif_label") for cond in range(conds)]
            self.visit(if_cond)
            self.instructions.append(f"jump_ifnot {elif_labels[0]}")
            self.visit(if_cond_true)
            self.instructions.append(f"jump {endif}")

            for ind in range(conds):
                self.instructions.append(f"{elif_labels[ind]}:")
                self.visit(elif_blocks[ind])
                if ind < conds-1:
                    self.instructions.append(f"jump_ifnot {elif_labels[ind+1]}")
                    self.visit(elif_blocks[ind + 1])
                    self.instructions.append(f"jump {endif}")
            #self.instructions.append(f"jump {else_label}")
            #self.instructions.append(f"{else_label}:")
            self.visit(else_block)
            #self.instructions.append(f"jump {endif}")
            self.instructions.append(f"{endif}:")


    # TODO:
    def while_block(self, tree):
        return tree

    def cond_and(self, tree):
        label = self.label("and")
        self.visit(tree.children[0])
        self.instructions.append(f"jump_ifnot {label}")
        self.visit(tree.children[1])
        self.instructions.append(f"{label}:")

    def cond_or(self, tree):
        tree.type = "Bool"
        return tree

    def cond_not(self, tree):
        tree.type = "Bool"

    def m_equal(self, tree):
        tree.type = "Bool"
        self.instructions.append(f"call {tree.children[0].type}:equals")

    def m_notequal(self, tree):
        tree.type = "Bool"

    def m_less(self, tree):
        self.instructions.append(f"roll 1")
        self.instructions.append(f"call {tree.children[0].type}:less")

    def m_more(self, tree):
        self.instructions.append(f"roll 1")
        self.instructions.append(f"call {tree.children[0].type}:more")

    def m_atmost(self, tree):
        self.instructions.append(f"roll 1")
        self.instructions.append(f"call {tree.children[0].type}:atmost")

    def m_atleast(self, tree):
        self.instructions.append(f"roll 1")
        self.instructions.append(f"call {tree.children[0].type}:atleast")

    def m_call(self, tree):
        #print(tree)
        #print(len(tree.children))
        #print(tree.children[0].type)
        #print(tree.children[1])
        #print()
        #self.visit(tree.children[0])
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
        self.instructions.append(f"const {tree.children[0]}")

    def lit_str(self, tree):
        self.instructions.append(f"const \"{tree.children[0]}\"")

    def m_neg(self, tree):
        self.instructions.append(f"call {tree.children[0].type}:negate")

    def var(self, tree: Tree):
        self.instructions.append(f"load {tree.children[0]}")

    def assignment(self, tree):
        var_name = tree.children[0]
        var_type = tree.children[1]
        var_op = tree.children[2]

        self.variables[var_name] = var_type
        self.instructions.append(f"store {var_name}")

    def inf_assignment(self, tree):
        var_name = tree.children[0]
        var_op = tree.children[1]

        try:
            self.variables[var_name] = tree.type
        except AttributeError:
            self.variables[var_name] = 'unknown'
        self.instructions.append(f"store {var_name}")

    def visit(self, tree):
        #print(f"tree.data = {tree.data}")
        if isinstance(tree, Tree):
            if tree.data == "if_block":
                self.if_block(tree)
            elif tree.data == "while_block":
                self.while_block(tree)
            elif tree.data == "assignment":
                self.assignment(tree)
            else:
                super().visit(tree)
        else:
            pass
            #print(tree)
            #super().visit(tree)


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
