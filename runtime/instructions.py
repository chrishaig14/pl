class RuntimeVisitor:
    def visit_DeclareI(self, declareI):
        env.define(self.id)

    def visit_AssignI(self, assignI):
        env.assign(assignI.id, assignI.val.construct(env))

    def visit_FunctionCallI(self, functionCallI):
        proc_val = env.get(self.id)

        if proc_val.builtin:
            print(Fore.CYAN, " CALLING BUILTIN WITH ARGS", Fore.RESET)
            print(Fore.CYAN, self.args, Fore.RESET)
            val = proc_val.body([env.get(arg) for arg in self.args])
            env.assign('__return__', val)
            return
        args_val = [env.get(arg) for arg in self.args]
        print("ARGS: ", self.args)
        env = proc_val.closure.copy()
        print("################PARAMETERS: ", proc_val.params)

        for i, param in enumerate(proc_val.params):
            env.define(param)
            env.assign(param, args_val[i])
            print("ASSIGNING: ", param, " VALUE: ", args_val[i])
        print(Back.GREEN)
        print(Fore.BLACK)
        print("ENV BEFORE RUNNING BODY OF ", self.id, ": ", env)
        print(Back.RESET)
        print(Fore.RESET)
        stack.enter()
        proc_val.body.run(env, stack)

    def visit_BlockI(self, blockI):
        for statement in reversed(self.statements):
            stack.push((statement, env))
    def visit_VariableI(self, variableI):
        return self.env.get(variableI.id)
    def visit_IfI(self, ifI):
        if env.get(self.cond_var):
            self.then.run(env, stack)

    def visit_ReturnI(self, returnI):
        env.assign("__return__", env.get(self.id))
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
