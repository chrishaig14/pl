from compiler import logger
from compiler.ScopeAnalyzer import ScopeAnalyzer
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
        program.accept(scope_analyzer)
