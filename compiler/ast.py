class Program:
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_program(self)


class Array:
    def __init__(self, values):
        self.values = values
        self.nodetype = "Array"

    def accept(self, visitor):
        return visitor.visit_array(self)


class Block:
    def __init__(self, statements):
        self.statements = statements
        self.nodetype = "Block"

    def accept(self, visitor):
        return visitor.visit_block(self)


class If:
    def __init__(self, cond, then):
        self.then = then
        self.cond = cond
        self.nodetype = "If"

    def accept(self, visitor):
        return visitor.visit_if(self)


class FunctionCall:
    def __init__(self, id, args):
        self.args = args
        self.id = id
        self.nodetype = "FunctionCall"

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class Expression:
    def __init__(self, first, op, second):
        self.first = first
        self.op = op
        self.second = second
        self.nodetype = "Expression"

    def accept(self, visitor):
        return visitor.visit_expression(self)


class Declaration:
    def __init__(self, id, init):
        self.init = init
        self.id = id


    def accept(self, visitor):
        return visitor.visit_declaration(self)


class String:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_string(self)


class Function:
    def __init__(self, params, statements):
        self.statements = statements
        self.params = params

    def accept(self, visitor):
        return visitor.visit_function(self)


class Return:
    def __init__(self, exp):
        self.exp = exp

    def accept(self, visitor):
        return visitor.visit_return(self)


class Variable:
    def __init__(self, id):
        self.id = id

    def accept(self, visitor):
        return visitor.visit_variable(self)


class Number:
    def __init__(self, number):
        self.number = number

    def accept(self, visitor):
        return visitor.visit_number(self)


class Assignment:
    def __init__(self, lvalue, rvalue):
        self.rvalue = rvalue
        self.lvalue = lvalue

    def accept(self, visitor):
        return visitor.visit_assignment(self)
