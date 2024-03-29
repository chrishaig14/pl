import collections
import copy

from colorama import Fore, Back

from compiler.linear_instructions import ArrayI, NumberI
from runtime.builtins import _print, _sum, _sub, _mul, _div, _booleq, _boolneq
from runtime.environment import Environment
# from runtime.instructions import *
from runtime.store import Store


class ProcVal:
    def __init__(self, params, body, closure, builtin=False):
        self.params = params
        self.body = body
        self.closure = closure
        self.builtin = builtin

    def __str__(self):
        return "PROC VAL"

    def __repr__(self):
        return self.__str__()


class Stack:
    def __init__(self):
        self.stack = collections.deque()
        self.call_stack = collections.deque()

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        return self.stack.pop()

    def empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

    def enter(self):
        self.call_stack.append(len(self.stack))

    def leave(self):
        last = self.call_stack.pop()
        while len(self.stack) != last:
            self.stack.pop()


class FunctionVal:
    def __init__(self, params, body, closure, builtin=False):
        self.params = params
        self.body = body
        self.closure = closure
        self.builtin = builtin

    def __str__(self):
        return "PROC VAL"

    def __repr__(self):
        return self.__str__()


class Runtime:

    def __init__(self):
        store = Store()
        self.globals = {}
        env = Environment(store, '0')

        builtin_print = ProcVal(None, _print, None, True)
        builtin_sum = ProcVal(None, _sum, None, True)
        builtin_sub = ProcVal(None, _sub, None, True)
        builtin_mul = ProcVal(None, _mul, None, True)
        builtin_div = ProcVal(None, _div, None, True)
        builtin_booleq = ProcVal(None, _booleq, None, True)
        builtin_boolneq = ProcVal(None, _boolneq, None, True)

        builtins = {}

        builtins['print'] = builtin_print
        builtins['sum'] = builtin_sum
        builtins['sub'] = builtin_sub
        builtins['mul'] = builtin_mul
        builtins['div'] = builtin_div
        builtins['booleq'] = builtin_booleq
        builtins['boolneq'] = builtin_boolneq

        env.define("__return__")

        self.stack = Stack()

        self.env = env

        self.store = store

        for name, proc in builtins.items():
            self.add_builtin(name, proc)

    def add_builtin(self, name, proc):
        # self.env.define(name)
        # self.env.assign(name, proc)
        self.globals[name] = proc

    def visit_DeclareI(self, declareI):
        # print("ENV BEFORE DECLARATION: ", self.env)
        self.env.define(declareI.name)
        # print("ENV AFTER DECLARATION: ", self.env)

    def visit_AssignI(self, assignI):

        # print("lvalue: ", type(assignI.lvalue))

        value = assignI.atom.accept(self)
        lvalue = assignI.lvalue.accept(self)
        print("ASSIGNING:")
        print("lvalue: ", lvalue)
        print("rvalue: ", value)
        self.store.assign(lvalue, value)

    def visit_FunctionI(self, functionI):
        # self.globals.define(functionI.name)
        print("DEFINING FUNCTION : ", functionI.name)
        funcVal = FunctionVal(functionI.params, functionI.statements, self.env.copy(), False)
        self.globals[functionI.name] = funcVal
        return funcVal

    def visit_ArrayI(self, arrayI):
        print("ARRAY VALUES: ", arrayI.values)
        return ArrayI([val.accept(self) for val in arrayI.values])

    def visit_MemberI(self, memberI):
        obj = self.env.get(memberI.exp)
        return obj.members.get(memberI.name)

    def visit_RefMemberI(self, refMemberI):
        obj = self.env.get(refMemberI.exp)
        return obj.members.getRef(refMemberI.name)

    def visit_RefVariableI(self, refVariableI):
        return self.env.getRef(refVariableI.name)

    def visit_NumberI(self, numberI):
        return numberI

    def visit_StringI(self, stringI):
        return stringI

    def visit_ObjectI(self, objectI):
        cop = copy.deepcopy(objectI)
        # env = self.env.copy()
        env = Environment(self.store, "ASD")
        k = 0
        for m in cop.members:
            env.define(m)
            env.assign(m, NumberI(k))
            k += 1
        cop.members = env
        return cop

    def visit_VariableI(self, variableI):

        value = self.env.get(variableI.name)
        print("VALUE OF VARIABLE: ", variableI.name, " :", value)
        return value

    def visit_MemberI(self, memberI):
        print("VISITING MEMBER: ", memberI.exp, " . ", memberI.name)
        obj = self.env.get(memberI.exp)
        print("OBJECT: ", obj)
        obj_member = obj.members.get(memberI.name)
        if obj_member is None:
            name = obj.class_name + "_" + memberI.name
            class_member = self.globals[name]
            print(name, " IS A CLASS MEMBER: ", class_member)
            return class_member
        print("IS AN OBJECT MEMBER: ", obj_member)
        return obj_member

    def visit_member(self, member):
        pass

    def visit_methodCallI(self, methodCallI):
        print("before accept mem: ", methodCallI.mem)
        # print("MEM EXP:", methodCallI.mem.exp)
        # obj = methodCallI.mem.exp
        # mem = methodCallI.mem.accept(self)
        obj = self.env.get(methodCallI.name)
        name = obj.class_name + "_" + methodCallI.mem
        class_member = self.globals[name]
        print(name, " IS A CLASS MEMBER: ", class_member)
        # return class_member


        # print("mem: ", mem)
        self.call_function(class_member,[methodCallI.name])

    def call_function(self, proc_val, functionCallargs):
        print("CALLINF PROC VAL:", proc_val)
        if proc_val.builtin:
            arguments = [self.env.get(arg) for arg in functionCallargs]
            val = proc_val.body(arguments)
            self.env.assign("__return__", val)
            print("RETURN FROM BULTIN: ", val)
            return val
        args_val = [self.env.get(arg) for arg in functionCallargs]
        env = proc_val.closure.copy()
        for i, param in enumerate(proc_val.params):
            env.define(param)
            env.assign(param, args_val[i])
        original_env = self.env
        self.env = env
        self.stack.enter()
        # print("ENVIRONMENT IN FUNCTION: ", self.env)
        proc_val.body.accept(self)
        # print("ENVIRONMENT IN FUNCTION AT THE END: ", self.env)
        # print("STORE IN FUNCTION AT THE END: ", self.store)
        self.env = original_env
        # self.stack.leave()

        returnvalue = self.env.get("__return__")

    def visit_functionCallI(self, functionCall):
        # print("CALLLLLLLLING FUNCTIIIIIIIIIIIIIIIIION")
        proc_val = self.globals[functionCall.name]
        self.call_function(proc_val, functionCall.args)
        # return returnvalue

    def visit_BlockI(self, blockI):
        # print("PUSHING BLOCK:")
        for statement in reversed(blockI.statements):
            # print("PUSHED: ", statement)
            self.stack.push((statement, self.env))

    def visit_IfI(self, ifI):
        if self.env.get(self.cond_var):
            self.then.run(self.env, self.stack)

    def visit_ReturnI(self, returnI):
        print("RETURNING NAME: ", returnI.name)
        value = returnI.name.accept(self)
        print("RETURNING VALUE: ", value)
        self.env.assign("__return__", value)
        self.stack.leave()

    def run(self, prog):
        stack = self.stack
        env = self.env
        store = self.store
        for s in reversed(prog):
            stack.push((s, env))
        while not stack.empty():
            x = stack.pop()
            statement, m_env = x
            self.env = m_env
            statement.accept(self)
