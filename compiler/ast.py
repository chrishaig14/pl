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
    def __init__(self, name, args):
        self.args = args
        self.name = name
        self.nodetype = "FunctionCall"

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class MethodCall:
    def __init__(self, mem, args):
        self.args = args
        self.mem = mem
        self.nodetype = "MethodCall"

    def accept(self, visitor):
        return visitor.visit_method_call(self)

class Expression:
    def __init__(self, first, op, second):
        self.first = first
        self.op = op
        self.second = second
        self.nodetype = "Expression"

    def accept(self, visitor):
        return visitor.visit_expression(self)


class NewObject:
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_newObject(self)



class Declaration:
    def __init__(self, name, init):
        self.init = init
        self.name = name
        self.nodetype = "Declaration"

    def accept(self, visitor):
        return visitor.visit_declaration(self)


class Member:
    def __init__(self, exp, name):
        self.exp = exp
        self.name = name
        self.nodetype = "Member"

    def accept(self, visitor):
        return visitor.visit_member(self)


class SetMember:
    def __init__(self, exp, name):
        self.exp = exp
        self.name = name
        self.nodetype = "SetMember"

    def accept(self, visitor):
        return visitor.visit_setMember(self)


class String:
    def __init__(self, value):
        self.value = value
        self.nodetype = "String"

    def accept(self, visitor):
        return visitor.visit_string(self)


class Function:
    def __init__(self, name, params, statements):
        self.name = name
        self.statements = statements
        self.params = params
        self.nodetype = "Function"

    def accept(self, visitor):
        return visitor.visit_function(self)


class Class:
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements
        self.nodetype = "Class"

    def accept(self, visitor):
        return visitor.visit_class(self)


class Return:
    def __init__(self, exp):
        self.exp = exp
        self.nodetype = "Return"

    def accept(self, visitor):
        return visitor.visit_return(self)


class Variable:
    def __init__(self, name):
        self.name = name
        self.nodetype = "Variable"

    def accept(self, visitor):
        return visitor.visit_variable(self)


class SetVariable:
    def __init__(self, name):
        self.name = name
        self.nodetype = "SetVariable"

    def accept(self, visitor):
        return visitor.visit_setVariable(self)


class Number:
    def __init__(self, number):
        self.number = number
        self.nodetype = "Number"

    def accept(self, visitor):
        return visitor.visit_number(self)


class Assignment:
    def __init__(self, lvalue, rvalue):
        self.rvalue = rvalue
        self.lvalue = lvalue
        self.nodetype = "Assignment"

    def accept(self, visitor):
        return visitor.visit_assignment(self)
