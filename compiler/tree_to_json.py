class TreeToJson:

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

    def visit_array(self, array):
        obj = {}
        obj["type"] = "array"
        obj["values"] = [st.accept(self) for st in array.values]
        return obj

    def visit_variable(self, variable):
        obj = {}
        obj["type"] = "variable"
        obj["id"] = variable.id
        return obj

    def visit_function(self, function):
        obj = {}
        obj["type"] = "function"
        obj["params"] = function.params
        obj["statements"] = function.statements.accept(self)
        return obj

    def visit_function_call(self, function_call):
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
    def visit_string(self, string):
        obj = {}
        obj["type"] = "string"
        obj["string"] = string.value
        return obj

    def visit_declaration(self, declaration):
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

    def visit_return(self, return_s):
        obj = {}
        obj["type"] = "return"
        obj["exp"] = return_s.exp.accept(self)
        return obj

    def visit_expression(self, expression):
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
