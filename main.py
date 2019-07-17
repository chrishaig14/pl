from compiler.compiler import Compiler
from runtime.runtime import Runtime, DeclarationInstr, AssignVarValInstr, BlockInstr, Proc, ProcCallInstr, IfInstr, \
    ReturnInstr, Number

source = open("sample1.aspl")
source = source.read()

print("SOURCE IS: ", source)

compiler = Compiler()
code = compiler.compile(source)

for line in code:
    print(line)

# runtime = Runtime()
# runtime.run(prog)
