import copy

counter = 0


def new_var():
    global counter
    name = "aux" + str(counter)
    counter += 1
    return name


class CodeI:
    def __repr__(self):
        return str(self)


class DeclareI(CodeI):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "DECLARE " + self.name


class AssignI(CodeI):
    def __init__(self, name, atom):
        self.name = name
        self.atom = atom

    def __str__(self):
        return "ASSIGN " + self.name + " " + str(self.atom)


class NumberI(CodeI):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class StringI(CodeI):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class FunctionCallI(CodeI):
    def __init__(self, name, args):
        self.args = args
        self.name = name

    def __str__(self):
        return "CALL " + self.name + str(self.args)


class VariableI(CodeI):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class ReturnI(CodeI):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "RETURN " + self.name


class FunctionI(CodeI):
    def __init__(self, params, statements):
        self.params = params
        self.statements = statements

    def __str__(self):
        return "FUNCTION " + str(self.params) + " " + str(self.statements)


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
        # code = ["FUNCTION " + str(function.statements.accept(self))]
        code = [FunctionI(function.params, function.statements.accept(self))]
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
        # code += ["CALL " + function_call.id + " " + self.to_string(arg_vars)]
        code += [FunctionCallI(function_call.id, arg_vars)]
        return code

    def visit_number(self, number):
        return str(number.number)

    def visit_string(self, string):
        return ["'" + string.value + "'"]

    def visit_declaration(self, declaration):
        print("VISITING DECLARATION")
        code = []
        code.append(DeclareI(declaration.id))
        if declaration.init is not None:
            code += declaration.init.accept(self)
            code[-1] = AssignI(declaration.id, code[-1])
            # code[-1] = declaration.id + " = " + code[-1]
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
        code += [ReturnI(return_var)]
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
