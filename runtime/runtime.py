import collections

from colorama import Fore, Back

from runtime.environment import Environment
from runtime.store import Store


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


class Instruction:
    def run(self, env, stack):
        pass


class DeclarationInstr(Instruction):
    def __init__(self, id: str):
        self.id = id

    def run(self, env, stack):
        print("run decl inst")
        env.define(self.id)

    def __str__(self):
        return "DECLARE" + " " + self.id


class AssignVarValInstr(Instruction):
    def __init__(self, id: str, val):
        self.id = id
        self.val = val

    def run(self, env, stack):
        print("run assign var val")
        env.assign(self.id, self.val.construct(env))

    def __str__(self):
        return "ASSIGN" + " " + self.id + " " + str(self.val)


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

    def __str__(self):
        return "ASSIGN" + " " + self.id + " " + self.var


class ProcCallInstr(Instruction):
    def __init__(self, id: str, args: [str]):
        self.id = id
        self.args = args

    def run(self, env, stack):
        proc_val = env.get(self.id)

        if proc_val.builtin:
            print(Fore.CYAN, " CALLING BUILTIN WITH ARGS", Fore.RESET)
            print(Fore.CYAN, self.args, Fore.RESET)
            val = proc_val.body([env.get(arg) for arg in self.args])
            # env.define('_return')
            # print("VALUE: ::", val)
            env.assign('__return__', val)
            return
        args_val = [env.get(arg) for arg in self.args]
        print("ARGS: ", self.args)
        # print("AND STORE: ", store)

        env = proc_val.closure.copy()
        print("################PARAMETERS: ", proc_val.params)

        for i, param in enumerate(proc_val.params):
            env.define(param)
            env.assign(param, args_val[i])
            print("ASSIGNING: ", param, " VALUE: ", args_val[i])
        # for statement in reversed(proc_val.body):
        #     # print("PUSHED: ", statement, "ENV: ", env)
        #     stack.push((statement, env))
        print(Back.GREEN)
        print(Fore.BLACK)
        print("ENV BEFORE RUNNING BODY OF ", self.id, ": ", env)
        # print("AND STORE: ", store)
        print(Back.RESET)
        print(Fore.RESET)
        stack.enter()
        proc_val.body.run(env, stack)

    def __str__(self):
        return "CALL" + " " + self.id + " " + str(self.args)


class BlockInstr(Instruction):
    def __init__(self, statements: [Instruction]):
        self.statements = statements

    def run(self, env, stack):
        # print(Fore.RED)

        # print("RUNNING BLOCK")
        # print(Fore.RESET)
        for statement in reversed(self.statements):
            # print("PUSHED: ", statement, "ENV: ", env)
            stack.push((statement, env))


class IfInstr(Instruction):
    def __init__(self, cond_var: str, then: [Instruction]):
        self.cond_var = cond_var
        self.then = then

    def run(self, env, stack):
        if env.get(self.cond_var):
            self.then.run(env, stack)


class ReturnInstr(Instruction):
    def __init__(self, id: str):
        self.id = id

    def run(self, env, stack):
        # print("ENV RETURN: ", env)
        # print("STORE RETURN: ", store)
        # print("RETURNING: ", self.id)
        env.assign("__return__", env.get(self.id))
        # print("RETURN NOW IS: ", env.get("__return__"))
        # print("ENV RETURN: ", env)
        # print("STORE RETURN: ", store)
        stack.leave()


class Number:
    def __init__(self, value):
        self.value = value

    def construct(self, env):
        return self

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


class String:
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
    print(Back.RED, "PRINT GREEN", Back.RESET)
    print(Back.GREEN, x, Back.RESET)


def _sum(x):
    print(x)
    return Number(x[0].value + x[1].value)


def _sub(x):
    print(x)
    return Number(x[0].value - x[1].value)


def _mul(x):
    print(x)
    return Number(x[0].value * x[1].value)


def _div(x):
    print(x)
    return Number(x[0].value / x[1].value)


def _booleq(x):
    print(x)
    return x[0].value == x[1].value


def _boolneq(x):
    print(x)
    return x[0].value != x[1].value


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

    def run(self, prog):
        stack = self.stack
        env = self.env
        store = self.store
        for s in reversed(prog):
            stack.push((s, env))
        while not stack.empty():
            x = stack.pop()
            statement, m_env = x
            print(Back.YELLOW + Fore.BLACK, "STAT: ", statement, Back.RESET + Fore.RESET)

            statement.run(m_env, stack)
            print(" ENV: ", m_env)
            print(" STORE: ", store)
        print(id(env), " ENV: ", env)
