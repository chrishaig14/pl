from compiler.compiler import Compiler
from runtime.runtime import Runtime, DeclarationInstr, AssignVarValInstr, BlockInstr, Proc, ProcCallInstr, IfInstr, \
    ReturnInstr, Number

prog = [
    DeclarationInstr('factorial'),  # var a;
    AssignVarValInstr('factorial', Proc(['n'], BlockInstr([
        DeclarationInstr('aux'),
        AssignVarValInstr('aux', Number(0)),
        ProcCallInstr('booleq', ['n', 'aux']),
        IfInstr('__return__',
                BlockInstr([DeclarationInstr('one'), AssignVarValInstr('one', Number(1)), ReturnInstr('one')])),
        DeclarationInstr('aux1'),
        AssignVarValInstr('aux1', Number(1)),
        ProcCallInstr('sub', ['n', 'aux1']),
        ProcCallInstr('factorial', ['__return__']),
        ProcCallInstr('mul', ['__return__', 'n']),
        ReturnInstr('__return__')
    ]
    ))),  # }
    DeclarationInstr('n'),
    AssignVarValInstr('n', Number(10)),
    ProcCallInstr('factorial', ['n'])
]

source = open("sample1.aspl")
source = source.read()

print("SOURCE IS: ", source)

compiler = Compiler()
compiler.compile(source)

# print("FINAL:")
#
# for x in prog:
#     print(x)

# runtime = Runtime()
# runtime.run(prog)
