from __future__ import annotations

from typing import Literal

from xdsl.builder import Builder
from xdsl.dialects.arith import ConstantOp
from xdsl.dialects.builtin import Float64Type, FloatAttr
from xdsl.ir import Attribute, OpResult, SSAValues
from xdsl.parser import IntegerAttr, IntegerType

from xdsljson.structs.codegen import Codegen


class ConstOp(Codegen):
    """Constant value operand."""

    type: Literal["const"] = "const"
    val: float | int
    size: int = 64

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        if isinstance(self.val, float):
            attr: FloatAttr[Float64Type] = FloatAttr(float(self.val), Float64Type())
            const_op = ConstantOp(attr)
        else:
            attr2: IntegerAttr = IntegerAttr(int(self.val), IntegerType(64))
            const_op = ConstantOp(attr2)

        builder.insert(const_op)
        return const_op.results
