
# import logger
from compiler import logger
from compiler.ast import make_ast_node
from compiler.parser import Parser
from compiler.scanner import Scanner
from compiler.translator import Translator

logger.ACTIVE = False
logger.DEBUG = True


class Compiler:
    def __init__(self):
        pass

    def compile(self, source):

        scanner = Scanner(source)

        parser = Parser(scanner)
        tree = parser.parse()

        # print("#####     PARSE TREE     #####")
        for statement in tree:
            print(statement)

        # print("##### PRESS ENTER TO RUN #####")
        # input()

        logger.ACTIVE = True
        logger.DEBUG = False

        prog = []

        for node in tree:
            # print("NODE before: ", node)
            node = make_ast_node(node)
            # print("NODE after: ", node)
            prog.append(node)
            # print(node)

        translator = Translator()
        ir = translator.translate(prog)
        return ir
