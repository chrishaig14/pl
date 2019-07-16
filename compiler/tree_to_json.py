class TreeToJson:
    def __init__(self):
        pass

    def visit_program(self, program):
        obj = {}
        obj["type"] = "program"
        obj["statements"] = [st.accept(self) for st in program.statements]
        return obj

    def visit_block(self, block):
        obj = {}
        obj["type"] = "block"
        obj["statements"] = [st.accept(self) for st in block.statements]
        return obj
        # print("VISITING BLOCK")
        # all = []
        # for statement in block.statements:
        #     c = statement.accept(self)
        #     all.append(c)
        # block.statements = all
        # print("BLOCK IS:", block)
        # return block

    def visit_array(self, array):
        obj = {}
        obj["type"] = "array"
        obj["values"] = [st.accept(self) for st in array.statements]
        return obj
        # pass

    def visit_variable(self, variable):
        obj = {}
        obj["type"] = "variable"
        obj["id"] = variable.id
        return obj
        # return variable.id

    def visit_function(self, function):
        # function.statements = function.statements.accept(self)
        # return function
        obj = {}
        obj["type"] = "function"
        obj["params"] = function.params
        obj["statements"] = function.statements.accept(self)
        return obj

    def visit_function_call(self, function_call):
        # print("VISITING FUNCTION CALL")
        # all = []
        # for arg in function_call.args:
        #     a = arg.accept(self)
        #     all.append(a)
        # function_call.args = all
        # return function_call
        obj = {}
        obj["type"] = "function call"
        obj["id"] = function_call.id
        obj["args"] = [arg.accept(self) for arg in function_call.args]
        return obj

    def visit_number(self, number):
        obj = {}
        obj["type"] = "number"
        obj["number"] = number.number
        return obj
        # return "NUMBER " + str(number.number)

    def visit_declaration(self, declaration):
        # print("VISITING DECLARATION")
        # if declaration.init:
        #     c = declaration.init.accept(self)
        #     declaration.init = c
        # return declaration
        obj = {}
        obj["type"] = "declaration"
        obj["id"] = declaration.id
        if declaration.init is not None:
            obj["init"] = declaration.init.accept(self)
        return obj

    def visit_if(self, ifst):
        obj = {}
        obj["type"] = "if"
        obj["cond"] = ifst.cond.accept(self)
        obj["then"] = ifst.then.accept(self)
        return obj
        # pass

    def visit_return(self, return_s):
        obj = {}
        obj["type"] = "return"
        obj["exp"] = return_s.exp.accept(self)
        return obj
        # exp = return_s.exp.accept(self)
        # return_s.exp = exp
        # return return_s

    def visit_expression(self, expression):
        # print("VISITING EXPRESSION  ")
        # fun_id = ""
        # if expression.op == "plus":
        #     fun_id = "sum"
        # if expression.op == "minus":
        #     fun_id = "sub"
        # fc = FunctionCall(None)
        # fc.id = fun_id
        # f = expression.first.accept(self)
        # s = expression.second.accept(self)
        # fc.args = [f, s]
        # return fc
        obj = {}
        obj["type"] = "expression"
        obj["first"] = expression.first.accept(self)
        obj["op"] = expression.op
        obj["second"] = expression.second.accept(self)
        return obj

    def visit_assignment(self, assignment):
        obj = {}
        obj["type"] = "assignment"
        obj["lvalue"] = assignment.lvalue.accept(self)
        obj["rvalue"] = assignment.rvalue.accept(self)
        return obj
