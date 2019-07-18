from colorama import Back

from compiler.linear_instructions import NumberI


def _print(x):
    print("**** CALLING PRINT WITH: ", x)
    print(Back.RED, "PRINT GREEN", Back.RESET)
    print(Back.GREEN, x, Back.RESET)


def _sum(x):
    # print(x)
    return NumberI(x[0].value + x[1].value)


def _sub(x):
    # print(x)
    return NumberI(x[0].value - x[1].value)


def _mul(x):
    # print(x)
    return NumberI(x[0].value * x[1].value)


def _div(x):
    # print(x)
    return NumberI(x[0].value / x[1].value)


def _booleq(x):
    # print(x)
    return x[0].value == x[1].value


def _boolneq(x):
    # print(x)
    return x[0].value != x[1].value