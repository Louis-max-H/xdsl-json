from __future__ import annotations

from typing import Literal, cast

from xdsl.builder import Builder
from xdsl.dialects.arith import ConstantOp
from xdsl.dialects.builtin import AnyFloat, FloatAttr, IntegerAttr, IntegerType
from xdsl.ir import Attribute, OpResult, SSAValues

from xdsljson.structs.codegen import Codegen
from xdsljson.types_interface.type_float import TypeFloat
from xdsljson.types_interface.type_int import TypeInt


class ConstOp(Codegen):
    """Constant value operand."""

    op: Literal["const"] = "const"
    val: float | int
    type: TypeFloat | TypeInt = TypeInt("i64")

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        mlir_type = self.type.get_type()

        if isinstance(mlir_type, TypeFloat):
            attr = FloatAttr(float(self.val), cast(AnyFloat, mlir_type))
            const_op = ConstantOp(attr)
        else:
            attr2 = IntegerAttr(int(self.val), cast(IntegerType, mlir_type))
            const_op = ConstantOp(attr2)

        builder.insert(const_op)
        return const_op.results
