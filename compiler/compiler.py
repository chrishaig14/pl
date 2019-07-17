import copy

from compiler import logger
from compiler.ScopeAnalyzer import ScopeAnalyzer
from compiler.generator import Generator
from compiler.parser import Parser
from compiler.scanner import Scanner
from compiler.tree_to_json import TreeToJson

logger.ACTIVE = False
logger.DEBUG = True


class Compiler:
    def __init__(self):
        pass

    def compile(self, source):
        scanner = Scanner(source)

        parser = Parser(scanner)
        program = parser.parse()

        tree_to_json = TreeToJson()
        obj = program.accept(tree_to_json)
        print(obj)

        logger.ACTIVE = True
        logger.DEBUG = False

        scope_analyzer = ScopeAnalyzer()

        program_copy = copy.deepcopy(program)

        program_copy.accept(scope_analyzer)

        generator = Generator()
        code = program.accept(generator)

        return code
