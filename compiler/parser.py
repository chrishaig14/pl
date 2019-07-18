from colorama import Fore, Back, Style

from compiler.ast import Expression, Declaration, Assignment, Function, String, Number, Array, FunctionCall, Variable, \
    If, Return, Block, Program


class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = ""
        self.previous_token = None

    def parse_assign_exp(self):
        lvalue = self.parse_expression()

        if self.match("assign"):
            rvalue = self.parse_expression()
            return Assignment(lvalue, rvalue)
        else:
            return lvalue

    def parse_declaration(self):
        # declaration => var id
        if self.check("var"):
            self.advance()
            self.expect("id")
            id = self.previous_token["data"]
            exp = None
            if self.check("assign"):
                self.advance()
                exp = self.parse_expression()
            return Declaration(id, exp)

    def parse_expression(self):
        exp = self.parse_math_exp()

        if self.check("eqop"):
            op = self.current_token["type"]
            self.advance()
            second = self.parse_math_exp()
            exp = Expression(exp, op, second)

        return exp

    def parse_math_exp(self):
        exp = self.parse_term()

        while self.check("plus") or self.check("minus"):
            op = self.current_token["type"]
            self.advance()
            second = self.parse_term()
            exp = Expression(exp, op, second)
        return exp

    def parse_term(self):
        # term => factor

        factor = self.parse_factor()
        if factor is not None:
            # term => factor * term
            if self.check('mult'):
                self.advance()
                term = self.parse_term()
                return Expression(factor, 'mult', term)
            if self.check('div'):
                self.advance()
                term = self.parse_term()
                return Expression(factor, 'div', term)
            return factor

    def parse_function(self):
        print("NOW PARSING A FUNCTION")
        self.expect("lparen")
        params = []
        if self.match("id"):
            params.append(self.previous_token["data"])
            while self.match("comma"):
                self.expect("id")
                params.append(self.previous_token["data"])  ### send only id

        self.expect("rparen")

        statements = self.parse_block()

        return Function(params, statements)

    def parse_factor(self):
        # factor => number

        if self.match('string'):
            return String(self.previous_token["data"][1:-1])
        if self.match('number'):
            return Number(self.previous_token["data"])
        if self.match("lsquare"):
            print("PARSING ARRAY")
            values = []
            while values == [] or self.check("comma"):
                if self.check("comma"):
                    self.advance()
                val = self.parse_expression()
                print("VAL: ", val)
                values.append(val)
            self.expect("rsquare")
            print("ARRAY VALUES: ", values)
            return Array(values)
        # factor => id
        if self.match("id"):

            id = self.previous_token["data"]

            if self.match("lparen"):
                if self.match("rparen"):

                    return FunctionCall(id, [])
                else:
                    arg = self.parse_expression()

                    args = [arg]
                    while self.match("comma"):
                        arg = self.parse_expression()
                        args.append(arg)

                    self.match("rparen")
                    return FunctionCall(id, args)
            else:

                return Variable(id)

        # factor => ( exp )
        if self.match("lparen"):
            exp = self.parse_expression()
            if exp is not None:
                self.expect("rparen")
                return exp
        if self.match("fun"):
            fun = self.parse_function()
            return fun

    def parse_block(self):
        self.expect("lbrace")
        statements = []
        while not self.check("rbrace"):
            statement = self.parse_statement()
            statements.append(statement)

        self.advance()
        return Block(statements)

    def parse_if(self):
        if self.check("if"):
            self.advance()
            self.expect("lparen")
            exp = self.parse_expression()
            self.expect("rparen")
            then = self.parse_block()
            return If(exp, then)

    def parse_statement(self):
        # statement => declaration;
        if self.check("var"):
            decl = self.parse_declaration()

            self.expect("semicolon")

            if decl is not None:
                return decl

        # statement => assign_exp;
        if self.check("id"):
            assign = self.parse_assign_exp()

            self.expect("semicolon")
            if assign is not None:
                return assign
        if self.check("return"):
            self.advance()
            exp = self.parse_expression()

            self.expect("semicolon")
            return Return(exp)
        if self.check("if"):
            ifst = self.parse_if()
            return ifst

        print("Error: expected statement, got", self.current_token["type"])

    def match(self, token):
        if self.check(token):
            self.advance()
            return True
        return False

    def expect(self, token):
        if self.match(token):
            pass
        else:
            print("<<<### ERROR: expected", token, "instead of",
                  self.current_token["type"], "at line", self.current_token["line"], "###>>>")

    def advance(self):
        self.previous_token = self.current_token
        self.current_token = self.scanner.get_next()
        self.current_token = {"type": self.current_token[0][0], "data": self.current_token[0]
        [1], "line": self.current_token[1], "col": self.current_token[2]}

    def check(self, token):
        if self.current_token["type"] == token:
            return True
        return False

    def parse_program(self):
        program = []
        while not self.check("eof"):
            statement = self.parse_statement()
            program.append(statement)
        return Program(program)

    def parse(self):
        self.current_token = self.scanner.get_next()
        self.current_token = {"type": self.current_token[0][0], "data": self.current_token[0]
        [1], "line": self.current_token[1], "col": self.current_token[2]}
        return self.parse_program()
