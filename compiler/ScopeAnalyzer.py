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

    def __init__(self, parent=None):
        self.parent = parent
        self.scope = set()
        self.id = Scope.scope_id
        Scope.scope_id += 1

    def add(self, name):
        if name in self.scope:
            print("ERROR: ", name, " already declared in scope")
            exit(1)
        self.scope.add(name)

    def remove(self, name):
        self.scope.pop(name)

    def get(self, name):
        return name in self.scope or (self.parent and self.parent.get(name))

    def snapshot(self):
        my_copy = Scope()
        my_copy.scope = copy.deepcopy(self.scope)
        return my_copy

    def to_json(self):
        json = self.scope
        return json

    def __repr__(self):
        return "SCOPE ID: " + str(self.id) + str(self.to_json())

    def enter(self):
        n = Scope(parent=self)
        # print("LEAVING CURRENT SCOPE: ", self.id, " GOING TO CHILD: ", n.id)
        return n

    def leave(self):
        # print("LEAVING CURRENT SCOPE: ", self.id, " GOING TO PARENT: ", self.parent.id)
        return self.parent


class ScopeAnalyzer:
    def enter(self):
        self.scope = self.scope.enter()

    def leave(self):
        self.scope = self.scope.leave()

    def __init__(self):
        self.scope = Scope()
        self.scope.add("print")

    def visit_program(self, program):
        print("visiting program, scope is:", self.scope)
        for st in program.statements:
            st.accept(self)

    def visit_block(self, block):
        print("VISITING BLOCK, scope is:", self.scope)

        # all = []
        # self.scope.enter()
        for statement in block.statements:
            # c = statement.accept(self)
            statement.accept(self)

            # all.append(c)

        # block.statements = all

        # return NodeWithScope(block, self.scope)
        # self.scope.leave()
        pass

    def visit_array(self, array):
        # return NodeWithScope(array, self.scope)
        pass

    def visit_variable(self, variable):
        if not self.scope.get(variable.name):
            print("ERROR: ", variable.name, "not defined in scope")
            exit(1)
        # return NodeWithScope(variable, self.scope)
        pass

    def visit_function(self, function):
        print("VISITING FUNCTION" + function.name, " scope is: ", self.scope)

        self.scope.add(function.name)
        self.enter()
        for param in function.params:
            self.scope.add(param)
        function.statements.accept(self)

        self.leave()
        print("leaving FUNCTION" + function.name, "scope is: ", self.scope)

    def visit_function_call(self, function_call):
        print("VISITING FUNCTION CALL", function_call.name)
        if not self.scope.get(function_call.name):
            print("ERROR: ", function_call.name, "not defined in scope")
            exit(1)
        # args = []
        for arg in function_call.args:
            arg.accept(self)
        print("LEAVING FUNCTION CALL", function_call.name)
        # arg = arg.accept(self)
        # args.append(arg)
        # function_call.args = args
        # return NodeWithScope(function_call, self.scope)

    def visit_class(self, class_s):
        print("VISITING CLASS, ", class_s.name)
        if self.scope.get(class_s.name):
            print("ERROR: ", class_s.name, " already defined in scope")
            exit(1)
        self.scope.add(class_s.name)
        self.enter()
        class_s.statements.accept(self)
        self.leave()

    def visit_newObject(self, newObject):
        pass

    def visit_number(self, number):
        # return NodeWithScope(number, self.scope)
        pass

    def visit_string(self, string):
        # return NodeWithScope(string, self.scope)
        pass

    def visit_declaration(self, declaration):
        print("VISITING DECLARATION")
        # parent_scope = self.scope
        # self.scope = self.scope.snapshot()
        # self.scope.enter()
        self.scope.add(declaration.name)
        if declaration.init is not None:
            # declaration.init = declaration.init.accept(self)
            declaration.init.accept(self)
        # return NodeWithScope(declaration, parent_scope)

    def visit_if(self, ifst):
        print("VISITING IF")
        # ifst.cond = ifst.cond.accept(self)
        # ifst.then = ifst.then.accept(self)
        ifst.cond.accept(self)
        self.scope.enter()
        ifst.then.accept(self)
        self.scope.leave()

        # return NodeWithScope(ifst, self.scope)

    def visit_return(self, return_s):
        print("VISITING RETURN, scope is: ", self.scope)
        # return_s.exp = return_s.exp.accept(self)
        return_s.exp.accept(self)

        # return NodeWithScope(return_s, self.scope)

    def visit_expression(self, expression):
        # expression.first = expression.first.accept(self)
        expression.first.accept(self)

        # expression.second = expression.second.accept(self)
        expression.second.accept(self)

        # return NodeWithScope(expression, self.scope)

    def visit_assignment(self, assignment):
        # assignment.rvalue = assignment.rvalue.accept(self)
        assignment.rvalue.accept(self)

        # return NodeWithScope(assignment, self.scope)
