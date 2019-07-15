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

    def to_json(self):
        json = {}
        json["type"] = "array"
        json["values"] = [s.to_json() for s in self.values]
        return json

    def __repr__(self):
        return str(self.to_json())


class Block:
    def __init__(self, node):
        self.statements = [make_ast_node(s) for s in node["statements"]]

    def accept(self, visitor):
        return visitor.visit_block(self)

    def to_json(self):
        json = {}
        json["type"] = "block"
        json["statements"] = []
        for s in self.statements:
            json["statements"].append(s.to_json())
        return json

    def __repr__(self):
        return str(self.to_json())


class If:
    def __init__(self, node):
        self.cond = make_ast_node(node["cond"])
        self.then = make_ast_node(node["then"])

    def accept(self, visitor):
        return visitor.visit_if(self)

    def to_json(self):
        json = {}
        json["type"] = "if"
        json["then"] = self.then.to_json()
        return json

    def __repr__(self):
        return str(self.to_json())


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

    def to_json(self):
        json = {}
        json["type"] = "function_call"
        json["args"] = []

        for arg in self.args:
            json["args"].append(arg.to_json())
        return json

    def __repr__(self):
        return str(self.to_json())


class Expression:
    def __init__(self, node):
        self.first = make_ast_node(node["first"])
        self.second = make_ast_node(node["second"])
        self.op = node["op"]

    def accept(self, visitor):
        return visitor.visit_expression(self)

    def to_json(self):
        json = {}
        json["type"] = "expression"
        json["first"] = self.first.to_json()
        json["second"] = self.second.to_json()
        return json

    def __repr__(self):
        return str(self.to_json())


class Declaration:
    def __init__(self, node):
        self.id = node["id"]
        self.init = make_ast_node(node["init"])

    def accept(self, visitor):
        return visitor.visit_declaration(self)

    def to_json(self):
        json = {}
        json["type"] = "declaration"
        json["id"] = self.id
        if self.init is not None:
            json["init"] = self.init.to_json()
        else:
            json["init"] = None
        return json

    def __repr__(self):
        return str(self.to_json())


class String:
    def __init__(self, node):
        self.string = node["value"]

    def accept(self, visitor):
        return self.string

    def to_json(self):
        json = {}
        json["type"] = "string"
        json["value"] = self.string
        return json

    def __repr__(self):
        return str(self.to_json())


class Function:
    def __init__(self, node):
        self.params = [par["data"] for par in node["params"]]
        self.statements = make_ast_node(node["statements"])

    def accept(self, visitor):
        return visitor.visit_function(self)

    def to_json(self):
        json = {}
        json["type"] = "function"
        json["params"] = self.params
        json["statements"] = [s.to_json() for s in self.statements]
        return json

    def __repr__(self):
        return str(self.to_json())


class Return:
    def __init__(self, node):
        self.exp = make_ast_node(node["exp"])

    def accept(self, visitor):
        return visitor.visit_return(self)

    def to_json(self):
        json = {}
        json["type"] = "return"
        json["exp"] = self.exp.to_json()
        return json

    def __repr__(self):
        return str(self.to_json())


class Variable:
    def __init__(self, node):
        self.id = node["id"]

    def accept(self, visitor):
        return visitor.visit_variable(self)

    def to_json(self):
        json = {}
        json["type"] = "variable"
        json["id"] = self.id
        return json

    def __repr__(self):
        return str(self.to_json())


class Number:
    def __init__(self, node):
        self.number = node["value"]

    def accept(self, visitor):
        return visitor.visit_number(self)

    def to_json(self):
        json = {}
        json["type"] = "number"
        json["value"] = self.number
        return json

    def __repr__(self):
        return str(self.to_json())


class Assignment:
    def __init__(self, node):
        self.lvalue = make_ast_node(node["lvalue"])
        self.rvalue = make_ast_node(node["rvalue"])

    def accept(self, visitor):
        return visitor.visit_assignment(self)

    def to_json(self):
        json = {}
        json["type"] = "assignment"
        json["id"] = self.lvalue
        json["exp"] = self.rvalue.to_json()
        return json

    def __repr__(self):
        return str(self.to_json())
