from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from xdsl.builder import Builder
from xdsl.dialects.arith import ConstantOp
from xdsl.dialects.builtin import IndexType, IntegerAttr
from xdsl.dialects.memref import AllocaOp, LoadOp, StoreOp
from xdsl.ir import Attribute, OpResult, SSAValue, SSAValues

from xdsljson.structs.codegen import CodegenOp
from xdsljson.structs.op_vartype import VarTypeOp

if TYPE_CHECKING:
    pass

variablesHeap: dict[str, SSAValue] = {}


def _zero_index(builder: Builder) -> SSAValue:
    """Insère une constante d'index 0 et retourne sa SSAValue."""
    zero = ConstantOp(IntegerAttr(0, IndexType()))
    builder.insert(zero)
    return zero.results[0]


class VarOp(CodegenOp):
    type: Literal["var"] = "var"
    name: str
    varType: VarTypeOp | None

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        if self.name not in variablesHeap:
            raise ValueError(f"{self.name} not found in variable heap")

        memref_val = variablesHeap[self.name]
        index = _zero_index(builder)
        op = LoadOp.get(memref_val, [index])
        builder.insert(op)
        return op.results

    def codegenSet(self, value: SSAValue, builder: Builder) -> SSAValue:
        if self.name not in variablesHeap:
            alloca = AllocaOp.get(value.type, shape=[1])
            builder.insert(alloca)
            variablesHeap[self.name] = alloca.results[0]

        index = _zero_index(builder)
        store = StoreOp.get(value, variablesHeap[self.name], [index])
        builder.insert(store)

        return value
