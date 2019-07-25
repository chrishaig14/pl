from colorama import Back

from compiler.compiler import Compiler
from runtime.runtime import Runtime

source = open("sample1.aspl")
source = source.read()

print("SOURCE IS: ", source)

compiler = Compiler()
code = compiler.compile(source)

print(Back.RED)

for line in code:
    print(line)
print(Back.RESET)

runtime = Runtime()
runtime.run(code)
