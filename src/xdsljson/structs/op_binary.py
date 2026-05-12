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
from xdsl.ir import Attribute, OpResult, SSAValues

from xdsljson.structs.codegen import Codegen, sameFormat
from xdsljson.structs.op_operator import OperatorOp
from xdsljson.structs.op_var import VarOp

if TYPE_CHECKING:
    from xdsljson.structs.base import BaseValue


class BinaryOp(Codegen):
    """Opération binaire composée de deux opérandes."""

    op: Literal["binary"] = "binary"
    lhs: BaseValue
    rhs: BaseValue
    ope: OperatorOp

    def _codegen_affectation(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        if not isinstance(self.lhs, VarOp):
            raise TypeError(f"lhs of affectation should be VarOp, got {type(self.lhs)}")
        return self.lhs.codegenSet(self.rhs.codegen(builder)[0], builder)

    def _codegen_standard(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        lhs:  SSAValues[OpResult[Attribute]] = self.lhs.codegen(builder)
        rhs: SSAValues[OpResult[Attribute]] = self.rhs.codegen(builder)

        # Check same format
        if not sameFormat(lhs, rhs):
            raise ValueError("lhs and rhs SSAValues dont match")

        # On applique terme à terme
        results: list[OpResult[Attribute]] = []
        for l_elem, r_elem in zip(lhs, rhs):
            match self.ope.value:
                case "+":
                    opAddiOp = AddiOp(l_elem, r_elem)
                    builder.insert(opAddiOp)
                    results.append(opAddiOp.result)
                case "-":
                    opMinSIOp = MinSIOp(l_elem, r_elem)
                    builder.insert(opMinSIOp)
                    results.append(opMinSIOp.result)
                case "*":
                    opMuliOp = MuliOp(l_elem, r_elem)
                    builder.insert(opMuliOp)
                    results.append(opMuliOp.result)
                case "/":
                    opDivSIOp = DivSIOp(l_elem, r_elem)
                    builder.insert(opDivSIOp)
                    results.append(opDivSIOp.result)
                case "<" | ">" | "==" | "<=" | ">=":
                    equivalent = {
                        "<": "slt",
                        "<=": "sle",
                        ">": "sgt",
                        ">=": "sge",
                        "==": "eq",
                        "!=": "neq"
                    }
                    opCmpiOp = CmpiOp(l_elem, r_elem, equivalent[self.ope.value])
                    builder.insert(opCmpiOp)
                    results.append(opCmpiOp.result)
                case "or":
                    opOrIOp = OrIOp(l_elem, r_elem)
                    builder.insert(opOrIOp)
                    results.append(opOrIOp.result)
                case "and":
                    opAndIOp = AndIOp(l_elem, r_elem)
                    builder.insert(opAndIOp)
                    results.append(opAndIOp.result)
                case "xor":
                    opXOrIOp = XOrIOp(l_elem, r_elem)
                    builder.insert(opXOrIOp)
                    results.append(opXOrIOp.result)
                case _:
                    raise TypeError(f"Operator {self} not supported")

        return SSAValues(results)


    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:

        if self.ope.value == "=":
            return self._codegen_affectation(builder)
        else:
            return self._codegen_standard(builder)



