from lark.visitors import Visitor_Recursive
from lark import Tree
from os import path


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
        self.instructions.append(f"roll 1")
        self.instructions.append(f"call {tree.type}:plus")
        return tree

    def m_sub(self, tree):
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
                else:
                    self.instructions.append(f"jump_ifnot {elif_labels[ind]}")
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

    def while_block(self, tree):
        cond_label = self.label("while_label")
        cond_true_label = self.label("while_true")
        self.instructions.append(f"jump {cond_label}")
        self.instructions.append(f"{cond_true_label}:")
        self.visit(tree.children[1])
        self.instructions.append(f"{cond_label}:")
        self.visit(tree.children[0])
        self.instructions.append(f"jump_if {cond_true_label}")

    def cond_and(self, tree):
        #label = self.label("and")
        label = self.label("and_label")
        self.visit(tree.children[0])
        self.instructions.append(f"jump_ifnot {label}")
        self.visit(tree.children[1])
        self.instructions.append(f"{label}:")

    # TODO: There's got to be a better way to do this
    def cond_or(self, tree):
        true_label = self.label("or_label")
        false_label = self.label("or_label")
        self.visit(tree.children[0])
        self.instructions.append(f"jump_if {true_label}")
        self.visit(tree.children[1])
        self.instructions.append(f"jump_if {true_label}")
        self.instructions.append(f"const false")
        self.instructions.append(f"jump {false_label}")
        self.instructions.append(f"{true_label}:")
        self.instructions.append(f"const true")
        self.instructions.append(f"{false_label}:")

    def cond_not(self, tree):
        #print(tree.children)
        self.visit(tree.children[0])
        #self.instructions.append(f"{tree.children[0].type}:negate")
        #self.instructions.append(f"call Boolean:negate")
        self.instructions.append(f"call {tree.type}:negate")

    def m_equal(self, tree):
        self.instructions.append(f"call {tree.children[0].type}:equals")

    def m_notequal(self, tree):
        pass

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

        self.visit(var_op)
        self.variables[var_name] = var_type
        self.instructions.append(f"store {var_name}")

    def bare_expr(self, tree):
        pass
        #self.instructions.append(f"pop")

    def visit(self, tree):
        #print(f"tree.data = {tree.data}")
        if isinstance(tree, Tree):
            if tree.data == "if_block":
                #self.if_block(tree)
                self._call_userfunc(tree)
            elif tree.data == "while_block":
                #self.while_block(tree)
                self._call_userfunc(tree)
            elif tree.data == "assignment":
                #self.assignment(tree)
                self._call_userfunc(tree)
            elif tree.data == "cond_and":
                self._call_userfunc(tree)
            elif tree.data == "cond_or":
                self._call_userfunc(tree)
            elif tree.data == "cond_not":
                self._call_userfunc(tree)
            else:
                super().visit(tree)
        else:
            print("not tree")
            #print(tree)
            #super().visit(tree)

    def __default__(self, tree):
        pass


def build(filename, instructions, variables):
    class_name = path.splitext(path.basename(filename))[0]

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
