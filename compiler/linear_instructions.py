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
    def __init__(self, lvalue, atom):
        self.lvalue = lvalue
        self.atom = atom

    def accept(self, visitor):
        return visitor.visit_AssignI(self)

    def __str__(self):
        return "ASSIGN " + str(self.lvalue) + " " + str(self.atom)


class NumberI(CodeI):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_NumberI(self)

    def __str__(self):
        return "Number(" + str(self.value) + ")"

class ArrayI(CodeI):
    def __init__(self, values):
        self.values = values

    def accept(self, visitor):
        return visitor.visit_ArrayI(self)

    def __str__(self):
        return "Array(" + str(self.values) + ")"


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

class MethodCallI(CodeI):
    def __init__(self, name, mem, args):
        self.args = args
        self.mem = mem
        self.name = name

    def accept(self, visitor):
        return visitor.visit_methodCallI(self)

    def __str__(self):
        return "METHOD CALL " + str(self.name) + "." + str(self.mem) + " " + str(self.args)




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
        return "Return(" + str(self.name)+")"


class BlockI(CodeI):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_BlockI(self)

    def __str__(self):
        return "BLOCK [" + str(self.statements) + "]"

class MemberI(CodeI):
    def __init__(self, exp, name):
        self.exp = exp
        self.name = name

    def accept(self, visitor):
        return visitor.visit_MemberI(self)

    def __str__(self):
        return "Member(" + self.exp + "." + str(self.name)+")"

class RefMemberI(CodeI):
    def __init__(self, exp, name):
        self.exp = exp
        self.name = name

    def accept(self, visitor):
        return visitor.visit_RefMemberI(self)

    def __str__(self):
        return "RefMember(" + self.exp + "." + self.name+")"

class RefVariableI(CodeI):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_RefVariableI(self)

    def __str__(self):
        return "RefVariable(" + self.name+")"

class FunctionI(CodeI):
    def __init__(self, name, params, statements):
        self.name = name
        self.params = params
        self.statements = statements
        self.builtin = False

    def accept(self, visitor):
        return visitor.visit_FunctionI(self)

    def __str__(self):
        return "Function(" + self.name + "," + str(self.params) + "," + str(self.statements)+")"

class ObjectI(CodeI):
    def __init__(self, class_name, members):
        self.members = members
        self.class_name = class_name

    def accept(self, visitor):
        return visitor.visit_ObjectI(self)

    def __str__(self):
        return "Object(" + self.class_name + "," + str(self.members)+")"

