import copy

from compiler.linear_instructions import *

counter = 0


def new_var():
    global counter
    name = "aux" + str(counter)
    counter += 1
    return name


def add_result(code):
    last = code[-1]
    var = new_var()
    code[-1] = DeclareI(var)
    code.append("")
    code[-1] = AssignI(var, last)
    return var


class LinearGenerator:

    def visit_program(self, program):
        code = []
        for st in program.statements:
            code += st.accept(self)
        return code

    def visit_block(self, block):
        print("VISITING BLOCK IN GENERATOR")

        code = []
        for st in block.statements:
            code += st.accept(self)
        return BlockI(code)

    def visit_array(self, array):
        print("VISITING ARRAY")
        code = []
        val_vars = []
        for val in array.values:
            val = val.accept(self)
            code += val
            arg_var = add_result(code)
            val_vars.append(VariableI(arg_var))
        code += [ArrayI(val_vars)]
        return code

    def visit_variable(self, variable):
        return [VariableI(variable.name)]

    def visit_function(self, function):
        print("VISITING FUNCTION")
        code = [FunctionI(function.name, function.params, function.statements.accept(self))]
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
        code += [FunctionCallI(function_call.name, arg_vars)]
        code += [VariableI("__return__")]
        return code

    def visit_number(self, number):
        return [NumberI(number.number)]

    def visit_string(self, string):
        print("VISITING STRING: ", string)
        return [StringI(string.value)]

    def visit_declaration(self, declaration):
        print("VISITING DECLARATION")
        code = []
        code.append(DeclareI(declaration.name))
        if declaration.init is not None:
            code += declaration.init.accept(self)
            code[-1] = AssignI(declaration.name, code[-1])
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
        return_var = add_result(code)
        code += [ReturnI(return_var)]
        return code

    def visit_expression(self, expression):
        code = []
        code += expression.first.accept(self)

        first_var = add_result(code)

        code += expression.second.accept(self)

        second_var = add_result(code)

        builtin = ""
        if expression.op == "plus":
            builtin = "sum"
        if expression.op == "minus":
            builtin = "sub"

        code += [FunctionCallI(builtin, [first_var, second_var])]
        return code

    def visit_assignment(self, assignment):
        code = assignment.rvalue.accept(self)
        rvalue = add_result(code)
        lvalue = assignment.lvalue.accept(self)
        code += [AssignI(assignment.lvalue.name, VariableI(rvalue))]
        return code
