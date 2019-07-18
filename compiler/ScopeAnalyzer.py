import copy


class NodeWithScope:
    def __init__(self, node, scope):
        self.node = node
        self.scope = scope

    def to_json(self):
        json = {}
        json["node"] = self.node.to_json()
        json["scope"] = self.scope.to_json()
        return json

    def __repr__(self):
        return str(self.to_json())


class Scope:
    scope_id = 0

    def __init__(self):
        self.scope = set()
        self.id = Scope.scope_id
        Scope.scope_id += 1

    def add(self, name):
        self.scope.add(name)

    def remove(self, name):
        self.scope.pop(name)

    def get(self, name):
        return name in self.scope

    def snapshot(self):
        my_copy = Scope()
        my_copy.scope = copy.deepcopy(self.scope)
        return my_copy

    def to_json(self):
        json = self.scope
        return json
    def __repr__(self):
        return str(self.to_json())


class ScopeAnalyzer:
    def __init__(self):
        self.scope = Scope()

    def visit_program(self, program):
        for st in program.statements:
            st.accept(self)

    def visit_block(self, block):
        print("VISITING BLOCK")

        all = []
        for statement in block.statements:
            c = statement.accept(self)
            all.append(c)

        block.statements = all

        return NodeWithScope(block, self.scope)

    def visit_array(self, array):
        return NodeWithScope(array, self.scope)

    def visit_variable(self, variable):
        if not self.scope.get(variable.name):
            print("ERROR: ", variable.name, "not defined in scope")
            exit(1)
        return NodeWithScope(variable, self.scope)

    def visit_function(self, function):
        print("VISITING FUNCTION")

        parent_scope = self.scope
        function_scope = self.scope.snapshot()

        self.scope = function_scope
        for param in function.params:
            function_scope.add(param)
        function.statements = function.statements.accept(self)

        self.scope = parent_scope

        return NodeWithScope(function, parent_scope)

    def visit_function_call(self, function_call):
        print("VISITING FUNCTION CALL")
        args = []
        for arg in function_call.args:
            arg = arg.accept(self)
            args.append(arg)
        function_call.args = args
        return NodeWithScope(function_call, self.scope)

    def visit_number(self, number):
        return NodeWithScope(number, self.scope)

    def visit_declaration(self, declaration):
        print("VISITING DECLARATION")
        parent_scope = self.scope
        self.scope = self.scope.snapshot()
        self.scope.add(declaration.id)
        if declaration.init is not None:
            declaration.init = declaration.init.accept(self)
        return NodeWithScope(declaration, parent_scope)

    def visit_if(self, ifst):
        print("VISITING IF")
        ifst.cond = ifst.cond.accept(self)
        ifst.then = ifst.then.accept(self)
        return NodeWithScope(ifst, self.scope)

    def visit_return(self, return_s):
        print("VISITING RETURN")
        return_s.exp = return_s.exp.accept(self)
        return NodeWithScope(return_s, self.scope)

    def visit_expression(self, expression):
        expression.first = expression.first.accept(self)
        expression.second = expression.second.accept(self)
        return NodeWithScope(expression, self.scope)

    def visit_assignment(self, assignment):
        assignment.rvalue = assignment.rvalue.accept(self)
        return NodeWithScope(assignment, self.scope)
