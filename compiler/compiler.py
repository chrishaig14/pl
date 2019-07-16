# import logger
from compiler import logger
from compiler.ScopeAnalyzer import ScopeAnalyzer
# from compiler.ast import make_ast_node
from compiler.extract_args_to_var import ExtractArgsToVar
from compiler.parser import Parser
from compiler.scanner import Scanner
from compiler.translator import FromOpToProcCall
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

        # print("#####     PARSE TREE     #####")
        # for statement in tree:
        #     print(statement)

        # print("##### PRESS ENTER TO RUN #####")
        # input()

        logger.ACTIVE = True
        logger.DEBUG = False

        # prog = []
        #
        # for node in tree:
        #     # print("NODE before: ", node)
        #     node = make_ast_node(node)
        #     # print("NODE after: ", node)
        #     prog.append(node)
        #     # print(node)

        # scope_analyzer = ScopeAnalyzer()
        #
        # ir = scope_analyzer.analyze(prog)

        # translator = FromOpToProcCall()
        # ir = translator.translate(prog)

        # translator = ExtractArgsToVar(ir)
        # ir = translator.translate(ir)

        # return ir
