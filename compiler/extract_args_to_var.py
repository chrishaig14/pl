class ExtractArgsToVar:
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
        pass

    def visit_function(self, function):
        function.statements = function.statements.accept(self)
        return function

    def visit_function_call(self, function_call):
        pass
        # print("VISITING FUNCTION CALL")
        # all = []
        # for arg in function_call.args:
        #     a = arg.accept(self)
        #     all.append(a)
        # function_call.args = all
        # return function_call

    def visit_number(self, number):
        pass

    def visit_declaration(self, declaration):
        pass

    def visit_if(self, ifst):
        pass

    def visit_return(self, return_s):
        pass

    def visit_expression(self, expression):
        pass

    def visit_assignment(self, assignment):
        pass
