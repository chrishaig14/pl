class CodeI:
    def __repr__(self):
        return str(self)


class DeclareI(CodeI):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_DeclareI(self)

    def __str__(self):
        return "DECLARE " + self.name


class AssignI(CodeI):
    def __init__(self, name, atom):
        self.name = name
        self.atom = atom

    def accept(self, visitor):
        return visitor.visit_AssignI(self)

    def __str__(self):
        return "ASSIGN " + self.name + " " + str(self.atom)


class NumberI(CodeI):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_NumberI(self)

    def __str__(self):
        return "Number(" + str(self.value) + ")"


class StringI(CodeI):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_StringI(self)

    def __str__(self):
        return "String(" + str(self.value) + ")"


class FunctionCallI(CodeI):
    def __init__(self, name, args):
        self.args = args
        self.name = name

    def accept(self, visitor):
        return visitor.visit_functionCallI(self)

    def __str__(self):
        return "CALL " + self.name + " " + str(self.args)


class VariableI(CodeI):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_VariableI(self)

    def __str__(self):
        return "Variable(" + self.name + ")"


class ReturnI(CodeI):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_ReturnI(self)

    def __str__(self):
        return "RETURN " + self.name


class BlockI(CodeI):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_BlockI(self)

    def __str__(self):
        return "BLOCK [" + str(self.statements) + "]"


class FunctionI(CodeI):
    def __init__(self, params, statements):
        self.params = params
        self.statements = statements
        self.builtin = False

    def accept(self, visitor):
        return visitor.visit_FunctionI(self)

    def __str__(self):
        return "FUNCTION " + str(self.params) + " " + str(self.statements)
