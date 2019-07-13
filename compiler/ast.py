from colorama import Fore, Back
import copy

counter = 0


def make_ast_node(node):
    if node is None:
        return None
    if node["type"] == "Declaration":
        return Declaration(node)
    if node["type"] == "Assignment":
        return Assignment(node)
    if node["type"] == "Expression":
        return Expression(node)
    if node["type"] == "Variable":
        return Variable(node)
    if node["type"] == "Number":
        return Number(node)
    if node["type"] == "String":
        return String(node)
    if node["type"] == "FunctionCall":
        return FunctionCall(node)
    if node["type"] == "Return":
        return Return(node)
    if node["type"] == "Function":
        return Function(node)
    if node["type"] == "If":
        return If(node)
    if node["type"] == "Block":
        return Block(node)
    if node["type"] == "Array":
        return Array(node)


class Array:
    def __init__(self, node):
        self.values = [make_ast_node(s) for s in node["values"]]

    def accept(self, visitor):
        return visitor.visit_array(self)

    def __str__(self):
        return "(array " + str([str(s) for s in self.values]) + ")"


class Block:
    def __init__(self, node):
        self.statements = [make_ast_node(s) for s in node["statements"]]

    def accept(self, visitor):
        return visitor.visit_block(self)

    def __str__(self):
        # print("PRINTING BLOCK")
        x = "(block "
        for s in self.statements:
            # print("STAT:", str(s))
            x += str(s)
        x += ")"
        # print("X: ", x)
        return x

    def __repr__(self):
        return str(self)


class If:
    def __init__(self, node):
        self.cond = make_ast_node(node["cond"])
        self.then = make_ast_node(node["then"])

    def accept(self, visitor):
        return visitor.visit_if(self)

    def __str__(self):
        return "(if " + str(self.cond) + " " + str(self.then) + ")"

    def __repr__(self):
        return str(self)


class FunctionCall:
    def __init__(self, node=None):
        if node is not None:
            self.id = node["id"]
            self.args = [make_ast_node(arg) for arg in node["args"]]
        else:
            self.id = ""
            self.args = []

    def accept(self, visitor):
        return visitor.visit_function_call(self)

    def __str__(self):
        string = "(function_call " + self.id + " ["
        for arg in self.args:
            string += str(arg) + ","
        string = string[:-1]
        string += "])"
        return string

    def __repr__(self):
        return str(self)


class Expression:
    def __init__(self, node):
        self.first = make_ast_node(node["first"])
        self.second = make_ast_node(node["second"])
        self.op = node["op"]

    def accept(self, visitor):
        return visitor.visit_expression(self)

    def __str__(self):
        return "(" + self.op + " " + str(self.first) + \
               " " + str(self.second) + ")"

    def __repr__(self):
        return str(self)


class Declaration:
    def __init__(self, node):
        self.id = node["id"]
        self.init = make_ast_node(node["init"])

    def accept(self, visitor):
        return visitor.visit_declaration(self)

    def __str__(self):
        return "(declare " + self.id + " " + str(self.init) + ")"

    def __repr__(self):
        return str(self)


class String:
    def __init__(self, node):
        self.string = node["value"]

    def accept(self, visitor):
        return self.string

    def __str__(self):
        return "(string " + self.string + ")"


class Function:
    def __init__(self, node):
        self.params = [par["data"] for par in node["params"]]
        self.statements = make_ast_node(node["statements"])
        # logger.debug(
        #     Back.YELLOW +
        #     Fore.BLACK,
        #     "NEW CLOSURE FOR FUNCTION",
        #     Back.RESET +
        #     Fore.RESET)
        # self.closure = env.copy()
        # self.closure.name = "CLOSURE FOR FUNCTION"
        # self.closure.store = env.store  # not SO DEEP COPY, MAINTAIN UNIQUE STORE
        # logger.debug(
        #     Back.RED +
        #     Fore.WHITE,
        #     "CLOSURE: ",
        #     self.closure,
        #     Back.RESET +
        #     Fore.RESET)

    def accept(self, visitor):
        return visitor.visit_function(self)

    def __str__(self):
        # return "FUN_STR"
        return "(fun " + str(self.params) + " " + \
               str(self.statements) + ")"

    def __repr__(self):
        return "FUN_REPR"


class Return:
    def __init__(self, node):
        self.exp = make_ast_node(node["exp"])

    def accept(self, visitor):
        return visitor.visit_return(self)

    def __str__(self):
        return "(return " + str(self.exp) + ")"


class Variable:
    def __init__(self, node):
        self.id = node["id"]

    def accept(self, visitor):
        return visitor.visit_variable(self)

    def __str__(self):
        return "(variable " + self.id + ")"


class Number:
    def __init__(self, node):
        self.number = node["value"]

    def accept(self, visitor):
        return visitor.visit_number(self)

    def __str__(self):
        return "(number " + str(self.number) + ")"


class Assignment:
    def __init__(self, node):
        self.lvalue = make_ast_node(node["lvalue"])
        self.rvalue = make_ast_node(node["rvalue"])

    def accept(self, visitor):
        return visitor.visit_assignment(self)

    def __str__(self):
        return "(assign " + str(self.lvalue) + " " + str(self.rvalue) + ")"

    def __repr__(self):
        return str(self)
