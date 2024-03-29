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
    code[-1] = AssignI(RefVariableI(var), last)
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

    def visit_setVariable(self, setVariable):
        return [RefVariableI(setVariable.name)]

    def visit_function(self, function):
        print("VISITING FUNCTION")
        code = [FunctionI(function.name, function.params, function.statements.accept(self))]
        return code

    def visit_setMember(self, setMember):
        code = setMember.exp.accept(self)
        res_var = add_result(code)
        code += [RefMemberI(res_var, setMember.name)]
        return code

    # code +=
    def visit_class(self, class_s):
        print("VISITING CLASS")
        members = []
        code = []
        for st in class_s.statements.statements:
            if st.nodetype == "Declaration":
                members.append(st.name)
            if st.nodetype == "Function":
                st.name = class_s.name + "_" + st.name
                st.params = ["my"] + st.params
                print("#### VISITING FUNCTION : ", st.name)
                code += st.accept(self)
        members = {x: None for x in members}
        code += [FunctionI(class_s.name + "_init", [], BlockI([
            DeclareI("new_object"),
            AssignI(RefVariableI("new_object"), ObjectI(class_s.name, members)),
            ReturnI(VariableI("new_object"))
        ]))]
        return code

    def to_string(self, arr):
        string = ""
        for a in arr:
            string += a + " "
        string = string[:-1]
        return string

    def visit_member(self, member):
        code = member.exp.accept(self)
        exp_var = add_result(code)
        code += [MemberI(exp_var, member.name)]
        return code

    def visit_method_call(self, method_call):
        print("VISITING FUNCTION CALL")
        code = []
        args = []
        arg_vars = []
        for arg in method_call.args:
            arg = arg.accept(self)
            code += arg
            arg_var = add_result(code)
            arg_vars.append(arg_var)
        code += method_call.mem.accept(self)
        # var = add_result(code)
        memexp= code[-1]

        code[-1] = MethodCallI(memexp.exp, memexp.name, arg_vars)
        code += [VariableI("__return__")]
        return code


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

    def visit_newObject(self, newObject):
        code = [FunctionCallI(newObject.name + "_init", [])]
        code += [VariableI("__return__")]
        return code

    def visit_declaration(self, declaration):
        print("VISITING DECLARATION")
        code = []
        code.append(DeclareI(declaration.name))
        if declaration.init is not None:
            code += declaration.init.accept(self)
            code[-1] = AssignI(RefVariableI(declaration.name), code[-1])
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
        code += [ReturnI(VariableI(return_var))]
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
        if expression.op == "mult":
            builtin = "mul"
        if expression.op == "div":
            builtin = "div"

        code += [FunctionCallI(builtin, [first_var, second_var])]
        code += [VariableI("__return__")]
        return code

    def visit_assignment(self, assignment):
        code = assignment.rvalue.accept(self)
        rvalue = add_result(code)
        lvalue = assignment.lvalue.accept(self)
        print("LVALUE CODE: ", lvalue[:-1])
        print("LVALUE CODE: ", lvalue[-1])
        code += lvalue[:-1]
        code += [AssignI(lvalue[-1], VariableI(rvalue))]
        return code
