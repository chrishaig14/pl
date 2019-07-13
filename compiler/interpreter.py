from colorama import Back, Fore

from environment import Environment
import logger
from store import Store


class Interpreter:
    def __init__(self, program):
        self.program = program
        self.store = Store()
        logger.debug(
            Back.YELLOW +
            Fore.BLACK,
            "NEW GLOBAL ENVIRONMENT",
            Back.RESET +
            Fore.RESET)
        self.environment = Environment(self.store, None, "GLOBAL")
        self.return_value = None
        self.set_return_val = False

    def run(self):
        for node in self.program:
            logger.debug(Back.CYAN + Fore.BLACK, node, Back.RESET + Fore.RESET)
            node.accept(self)
            logger.debug(self.environment)

    def visit_block(self, block):
        for statement in block.statements:
            statement.accept(self)
            if self.set_return_val:
                return

    def visit_array(self, array):
        return [v.accept(self) for v in array.values]

    def visit_variable(self, variable):
        return self.environment.get(variable.id)

    def visit_function(self, function):
        closure = self.environment.copy()
        closure.name = "CLOSURE FOR FUNCTION"
        closure.store = self.environment.store  # not SO DEEP COPY, MAINTAIN UNIQUE STORE
        return {"function": function, "closure": closure}

    def visit_function_call(self, function_call):
        logger.debug(Back.RED, "RUN", Back.RESET, function_call)
        args = [arg.accept(self) for arg in function_call.args]
        if function_call.id == "print":
            logger.log(Back.GREEN + Fore.BLACK, args[0], Back.RESET + Fore.RESET)
            return

        d = self.environment.get(function_call.id)
        function = d["function"]
        closure = d["closure"]

        print("FUNCTION: ", d)

        parent = self.environment
        new = closure.copy()
        new.name = "ENVIRONMENT FOR " + function_call.id
        logger.debug(
            Back.YELLOW + Fore.BLACK,
            "NEW ENVIRONMENT FOR FUNCTION: ",
            function_call.id,
            Back.RESET + Fore.RESET)
        new.store = self.environment.store
        new.parent = parent
        self.environment = new
        logger.debug(
            Back.RED,
            "CALLING FUNCTION",
            function_call.id,
            " WITH ENVIRONMENT", new,
            Back.RESET)
        for i in range(len(function.params)):
            param = function.params[i]
            arg = args[i]
            logger.debug("PARAM:", param)
            logger.debug("ARG:", arg)
            self.environment.define(param)
            self.environment.assign(param, arg)
        for stat in function.statements:

            stat.accept(self)
            print("EXECUTED: ", stat)
            print("RET VAL: ", self.return_value)
            if self.set_return_val:
                self.set_return_val = False

                name = self.environment.parent.name
                self.environment.parent.name = "PARENT"
                self.environment = self.environment.parent
                self.environment.name = name
                print("FUNCTION RETURNING: ", self.return_value)
                return self.return_value

    def visit_declaration(self, declaration):
        logger.debug(Back.RED, "RUN", Back.RESET, declaration)
        self.environment.define(declaration.id)
        if declaration.init is not None:
            val = declaration.init.accept(self)
            self.environment.assign(declaration.id, val)

    def visit_if(self, ifst):
        cond_result = ifst.cond.accept(self)
        if cond_result:
            print("EXECUTING IF")
            new = self.environment.copy()
            new.parent = self.environment
            self.environment = new
            ifst.then.accept(self)
            self.environment = new.parent
        else:
            print("NOT EXECUTING IF")

    def visit_return(self, return_s):
        logger.debug(Back.RED, "RUN", Back.RESET, return_s)
        val = return_s.exp.accept(self)
        self.return_value = val
        # print("RETURN STAT: ", return_s)
        # print("RETURN VALUE IS: ", self.return_value)
        self.set_return_val = True
        return val

    def visit_expression(self, expression):
        xxx = expression.first.accept(self)
        second = expression.second.accept(self)
        if expression.op == "plus":
            r = xxx + second
            return r
        if expression.op == "minus":
            return xxx - second
        if expression.op == "eqop":
            return xxx == second
        if expression.op == "mult":
            return xxx * second
        if expression.op == "div":
            return xxx / second

    def visit_assignment(self, assignment):
        logger.debug(Back.RED, "RUN", Back.RESET, assignment)
        val = assignment.rvalue.accept(self)
        self.environment.assign(assignment.lvalue.id,
                                val)
