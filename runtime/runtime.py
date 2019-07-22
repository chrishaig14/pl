import collections

from colorama import Fore, Back

from compiler.linear_instructions import ArrayI
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
        self.env.define(name)
        self.env.assign(name, proc)

    def visit_DeclareI(self, declareI):
        self.env.define(declareI.name)

    def visit_AssignI(self, assignI):
        print("ATOM: ", type(assignI.atom))
        value = assignI.atom.accept(self)
        self.env.assign(assignI.name, value)

    def visit_FunctionI(self, functionI):
        self.env.define(functionI.name)
        funcVal = FunctionVal(functionI.params, functionI.statements, self.env.copy(), False)
        self.env.assign(functionI.name, funcVal)
        return funcVal

    def visit_ArrayI(self, arrayI):
        print("ARRAY VALUES: ", arrayI.values)
        return ArrayI([val.accept(self) for val in arrayI.values])

    def visit_NumberI(self, numberI):
        return numberI

    def visit_StringI(self, stringI):
        return stringI

    def visit_ObjectI(self, objectI):
        return objectI

    def visit_VariableI(self, variableI):

        value = self.env.get(variableI.name)
        print("VALUE OF VARIABLE: ", variableI.name, " :",value)
        return value

    def visit_functionCallI(self, functionCall):
        proc_val = self.env.get(functionCall.name)
        if proc_val.builtin:
            arguments = [self.env.get(arg) for arg in functionCall.args]
            val = proc_val.body(arguments)
            self.env.assign("__return__", val)
            return val
        args_val = [self.env.get(arg) for arg in functionCall.args]
        env = proc_val.closure.copy()
        for i, param in enumerate(proc_val.params):
            env.define(param)
            env.assign(param, args_val[i])
        original_env = self.env
        self.env = env
        self.stack.enter()
        proc_val.body.accept(self)
        self.env = original_env

        returnvalue = self.env.get("__return__")
        return returnvalue

    def visit_BlockI(self, blockI):
        for statement in reversed(blockI.statements):
            self.stack.push((statement, self.env))

    def visit_IfI(self, ifI):
        if self.env.get(self.cond_var):
            self.then.run(self.env, self.stack)

    def visit_ReturnI(self, returnI):
        value = self.env.get(returnI.name)
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
