from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from xdsl.builder import Builder
from xdsl.dialects.arith import (
    AddiOp,
    AndIOp,
    CmpiOp,
    DivSIOp,
    MinSIOp,
    MuliOp,
    OrIOp,
    XOrIOp,
)
from xdsl.ir import Attribute, OpResult, SSAValue, SSAValues

from xdsljson.structs.codegen import CodegenOp
from xdsljson.structs.op_operator import OperatorOp
from xdsljson.structs.op_var import VarOp

if TYPE_CHECKING:
    from xdsljson.structs.base import BaseOp


class BinaryOp(CodegenOp):
    """Opération binaire composée de deux opérandes."""

    type: Literal["binary"] = "binary"
    lhs: BaseOp
    rhs: BaseOp
    op: OperatorOp

    def _codegen_affectation(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        if not isinstance(self.lhs, VarOp):
            raise TypeError(f"lhs of affectation should be VarOp, got {type(self.lhs)}")
        return self.lhs.codegenSet(self.rhs.codegen(builder), builder)

    def _codegen_standard(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        lhs:  SSAValues[OpResult[Attribute]] = self.lhs.codegen(builder)
        rhs: SSAValues[OpResult[Attribute]] = self.rhs.codegen(builder)

        match self.op.value:
            case "+":
                op = AddiOp(lhs, rhs)
            case "-":
                op = MinSIOp(lhs, rhs)
            case "*":
                op = MuliOp(lhs, rhs)
            case "/":
                op = DivSIOp(lhs, rhs)
            case "<" | ">" | "==" | "<=" | ">=":
                equivalent = {
                    "<": "slt",
                    "<=": "sle",
                    ">": "sgt",
                    ">=": "sge",
                    "==": "eq",
                    "!=": "neq"
                }
                op = CmpiOp(lhs, rhs, equivalent[self.op.value])
            case "or":
                op = OrIOp(lhs, rhs)
            case "and":
                op = AndIOp(lhs, rhs)
            case "xor":
                op = XOrIOp(lhs, rhs)
            case _:
                raise TypeError(f"Operator {self} not supported")

        builder.insert(op)
        return op.results


    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:

        if self.op.value == "=":
            return self._codegen_affectation(builder)
        else:
            return self._codegen_standard(builder)



