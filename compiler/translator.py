from colorama import Back, Fore

from compiler import logger
from compiler.ast import FunctionCall


class Translator:
    def __init__(self):
        pass

    def translate(self, tree):
        all = []
        for node in tree:
            c = node.accept(self)
            all.append(c)
        print(all)
        return all

    def visit_block(self, block):
        print("VISITING BLOCK")
        all = []
        for statement in block.statements:
            c = statement.accept(self)
            all.append(c)
        block.statements = all
        print("BLOCK IS:", block)
        return block

    def visit_array(self, array):
        pass

    def visit_variable(self, variable):
        return variable.id

    def visit_function(self, function):
        function.statements = function.statements.accept(self)
        return function

    def visit_function_call(self, function_call):
        print("VISITING FUNCTION CALL")
        all = []
        for arg in function_call.args:
            a = arg.accept(self)
            all.append(a)
        function_call.args = all
        return function_call

    def visit_number(self, number):
        return "NUMBER " + str(number.number)

    def visit_declaration(self, declaration):
        print("VISITING DECLARATION")
        if declaration.init:
            c = declaration.init.accept(self)
            declaration.init = c
        return declaration

    def visit_if(self, ifst):
        pass

    def visit_return(self, return_s):
        exp = return_s.exp.accept(self)
        return_s.exp = exp
        return return_s

    def visit_expression(self, expression):
        print("VISITING EXPRESSION  ")
        fun_id = ""
        if expression.op == "plus":
            fun_id = "sum"
        if expression.op == "minus":
            fun_id = "sub"
        fc = FunctionCall(None)
        fc.id = fun_id
        f = expression.first.accept(self)
        s = expression.second.accept(self)
        fc.args = [f, s]
        return fc

    def visit_assignment(self, assignment):
        pass
