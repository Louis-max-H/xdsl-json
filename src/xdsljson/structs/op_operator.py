from enum import Enum


class OperatorOp(str, Enum):
    plusOp = "+"
    minusOp = "-"
    timesOp = "*"
    divideOp = "/"
    powerOp = "^"
    andOp = "and"
    orOp = "or"
    xorOp = "xor"
    notOp = "not"
    equalsOp = "=="
    gtOp = ">"
    ltOp = "<"
    getOp = ">="
    letOp = "<="
