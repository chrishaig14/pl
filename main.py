import collections

from colorama import Fore

from environment import Environment
from store import Store


class Stack:
    def __init__(self):
        self.stack = collections.deque()

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        return self.stack.pop()

    def empty(self):
        return len(self.stack) == 0


class Instruction:
    def run(self, env, stack):
        pass


class DeclarationInstr(Instruction):
    def __init__(self, id: str):
        self.id = id

    def run(self, env, stack):
        print("run decl inst")
        env.define(self.id)


class AssignVarValInstr(Instruction):
    def __init__(self, id: str, val):
        self.id = id
        self.val = val

    def run(self, env, stack):
        print("run assign var val")
        env.assign(self.id, self.val.construct(env))


class AssignVarVarInstr(Instruction):
    def __init__(self, id: str, var: id):
        self.id = id
        self.var = var

    def run(self, env, stack):
        print(Fore.RED)
        print("ASSIGNING ", self.id, " = ", self.var)
        print(Fore.RESET)
        env.assign(self.id, env.get(self.var))
        print("D IS: ", env.get('d'))


class ProcCallInstr(Instruction):
    def __init__(self, id: str, args: [str]):
        self.id = id
        self.args = args

    def run(self, env, stack):
        proc_val = env.get(self.id)

        if proc_val.builtin:
            print(Fore.CYAN, " CALLING ", Fore.RESET)
            val = proc_val.body([env.get(arg) for arg in self.args])
            # env.define('_return')
            # print("VALUE: ::", val)
            env.assign('__return__', val)
            return

        env = proc_val.closure.copy()
        print("################PARAMETERS: ", proc_val.params)
        args_val = [env.get(arg) for arg in self.args]
        for i, param in enumerate(proc_val.params):
            env.define(param)
            env.assign(param, args_val[i])
        for statement in reversed(proc_val.body):
            # print("PUSHED: ", statement, "ENV: ", env)
            stack.push((statement, env))


class ReturnInstr(Instruction):
    def __init__(self, id: str):
        self.id = id

    def run(self, env, stack):
        env.assign("__return__", env.get(self.id))


class Number:
    def __init__(self, value):
        self.value = value

    def construct(self, env):
        return self

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


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


class Proc:
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def construct(self, env):
        return ProcVal(self.params, self.body, env.copy())


def _print(x):
    print(Fore.RED, "PRINT GREEN", Fore.RESET)
    print(Fore.GREEN, x, Fore.RESET)


def _sum(x):
    print(x)
    return x[0].value + x[1].value


def _sub(x):
    print(x)
    return x[0].value - x[1].value


def _booleq(x):
    print(x)
    return x[0].value == x[1].value


def _boolneq(x):
    print(x)
    return x[0].value != x[1].value


builtin_print = ProcVal(None, _print, None, True)
builtin_sum = ProcVal(None, _sum, None, True)
builtin_sub = ProcVal(None, _sub, None, True)
builtin_booleq = ProcVal(None, _booleq, None, True)
builtin_boolneq = ProcVal(None, _boolneq, None, True)

store = Store()

env = Environment(store, '0')

env.define('print')
env.assign('print', builtin_print)

env.define('sum')
env.assign('sum', builtin_sum)

env.define('sub')
env.assign('sub', builtin_sub)

env.define('booleq')
env.assign('booleq', builtin_booleq)

env.define('boolneq')
env.assign('boolneq', builtin_boolneq)

stack = Stack()

env.define("__return__")

prog = [
    (DeclarationInstr('a'), env),  # var a;
    (AssignVarValInstr('a', Number(21)), env),  # a = 2;
    (DeclarationInstr('b'), env),  # var b;
    (AssignVarVarInstr('b', 'a'), env),  # b = a;
    (AssignVarValInstr('b', Proc(['d'], [DeclarationInstr('aux'),  # b = proc(d) {
                                         AssignVarValInstr('aux', Number(5)),  # var aux = 5;
                                         ProcCallInstr('sum', ['d', 'aux']),  # d = sum(d,aux)
                                         AssignVarVarInstr('d', '__return__'),  # return d;
                                         ReturnInstr('d')])), env),  # }
    # b = proc (d) {d = d + 7; return d;};
    (DeclarationInstr('c'), env),  # var c;
    (AssignVarValInstr('c', Number(7)), env),  # c = 7;
    (ProcCallInstr('b', ['a']), env),  # b(a)
    (DeclarationInstr('x'), env),
    (DeclarationInstr('y'), env),
    (AssignVarValInstr('x', Number(9)), env),  # c = 7;
    (AssignVarValInstr('y', Number(7)), env),  # c = 7;
    (ProcCallInstr('boolneq', ['x', 'y']), env)
]

for s in reversed(prog):
    stack.push(s)

while not stack.empty():
    x = stack.pop()
    print("X: ", x)
    statement, m_env = x
    print("STAT: ", statement)
    print(id(m_env), " ENV: ", m_env)
    statement.run(m_env, stack)
    print(store)
    print(id(m_env), " ENV: ", m_env)
    # print(statement)
print(id(env), " ENV: ", env)
