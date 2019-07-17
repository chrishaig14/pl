import copy

counter = 0


def new_var():
    global counter
    name = "aux" + str(counter)
    counter += 1
    return name


def add_result(code):
    last = code[-1]
    var = new_var()
    code[-1] = "DECLARE " + var
    code.append("")
    code[-1] = var + " = " + last
    return var


class Generator:

    def visit_program(self, program):
        print("## VISITING PROGRAM")
        code = []
        for st in program.statements:
            code += st.accept(self)
        return code

    def visit_block(self, block):
        print("VISITING BLOCK")

        code = []
        for st in block.statements:
            code += st.accept(self)
        return code

    def visit_array(self, array):
        code = []
        values = []
        for val in array.values:
            code += val.accept(self)
            value_var = add_result(code)
            values += [value_var]
        string = "["
        for value in values:
            string += value + ","
        string = string[:-1]
        string += "]"
        code += [string]
        return code

    def visit_variable(self, variable):
        return variable.id

    def visit_function(self, function):
        print("VISITING FUNCTION")
        code = ["FUNCTION " + str(function.statements.accept(self))]
        return code

    def to_string(self, arr):
        string = ""
        for a in arr:
            string += a + " "
        string = string[:-1]
        return string

    def visit_function_call(self, function_call):
        print("VISITING FUNCTION CALL")
        code = []
        args = []
        arg_vars = []
        for arg in function_call.args:
            arg = arg.accept(self)
            code += arg
            arg_var = add_result(code)
            arg_vars.append(arg_var)
        code += ["CALL " + function_call.id + " " + self.to_string(arg_vars)]
        return code

    def visit_number(self, number):
        return str(number.number)

    def visit_string(self, string):
        return ["'" + string.value + "'"]

    def visit_declaration(self, declaration):
        print("VISITING DECLARATION")
        code = []
        code.append("DECLARE " + declaration.id)
        if declaration.init is not None:
            code += declaration.init.accept(self)
            code[-1] = declaration.id + " = " + code[-1]
        return code

    def visit_if(self, ifst):
        print("VISITING IF")
        code = []
        code += ifst.cond.accept(self)
        cond_var = add_result(code)
        code += ["IF " + cond_var + " " + str(ifst.then.accept(self))]
        return code

    def visit_return(self, return_s):
        print("VISITING RETURN")
        code = []
        code += return_s.exp.accept(self)
        # return_var = new_var()
        return_var = add_result(code)
        code += ["RETURN " + return_var]
        return code

    def visit_expression(self, expression):
        code = []
        code += expression.first.accept(self)

        first_var = add_result(code)

        code += expression.second.accept(self)

        second_var = add_result(code)

        code.append(first_var + " " + expression.op + " " + second_var)
        return code

    def visit_assignment(self, assignment):
        code = assignment.rvalue.accept(self)
        rvalue = add_result(code)
        code += [assignment.lvalue.accept(self) + " = " + rvalue]
        return code