from colorama import Back

from compiler.linear_instructions import NumberI


def _print(x):
    print(Back.RED, "PRINT GREEN", Back.RESET)
    print(Back.GREEN, x, Back.RESET)


def _sum(x):
    return NumberI(x[0].value + x[1].value)


def _sub(x):
    return NumberI(x[0].value - x[1].value)


def _mul(x):
    return NumberI(x[0].value * x[1].value)


def _div(x):
    return NumberI(x[0].value / x[1].value)


def _booleq(x):
    return x[0].value == x[1].value


def _boolneq(x):
    return x[0].value != x[1].value