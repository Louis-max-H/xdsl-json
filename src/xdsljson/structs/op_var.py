from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Literal

from pydantic import ConfigDict
from xdsl.builder import Builder
from xdsl.dialects.arith import ConstantOp
from xdsl.dialects.builtin import IndexType, MemRefType
from xdsl.dialects.func import FuncOp
from xdsl.dialects.memref import AllocaOp, LoadOp, StoreOp, SubviewOp
from xdsl.ir import Attribute, OpResult, SSAValue, SSAValues
from xdsl.rewriter import InsertPoint

from xdsljson.structs.codegen import Codegen
from xdsljson.structs.type_basic import TypeBasic

if TYPE_CHECKING:
    from xdsljson.structs.type_struct import TypeStruct

variablesHeap: dict[str, SSAValue] = {} # variable: OpResult[MemRefType[Attribute]]


def _index_const(builder: Builder, n: int = 0) -> SSAValue:
    op = ConstantOp.from_int_and_width(n, IndexType())
    builder.insert(op)
    return op.result


def _get_subview(
    name: str,
    indices: Sequence[SSAValue | int],
    builder: Builder
) -> OpResult[MemRefType[Attribute]]:
    assert name in variablesHeap.keys()
    memref_slot: SSAValue = variablesHeap[name]

    sub = SubviewOp.get(
        memref_slot,
        indices, # Offset
        [1],     # Size
        [1],     # Strides
        memref_slot.type
    )
    builder.insert(sub)
    return sub.result


def populate_block_heap(func: FuncOp):
    block = func.body.block
    builder = Builder(InsertPoint.at_end(block))

    for arg in func.args:
        assert arg.name_hint is not None
        name = arg.name_hint

        alloca = AllocaOp.get(arg.type, shape=[1])
        builder.insert(alloca)
        memref_slot = alloca.memref
        variablesHeap[name] = memref_slot

        rank0 = _get_subview(name, [0], builder)
        i0 = _index_const(builder, 0)
        store = StoreOp.get(arg, rank0, [i0])
        builder.insert(store)

class VarOp(Codegen):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: Literal["var"] = "var"
    name: str
    attributeType: TypeBasic | TypeStruct | None = None

    def get_type(self) -> Attribute:
        # type already exist
        if self.name in variablesHeap.keys():
            return variablesHeap[self.name].type

        # Codegen type
        assert self.attributeType is not None
        return self.attributeType.get_type()

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        if self.name not in variablesHeap:
            raise ValueError(f"{self.name} not found in variable heap")

        index = _get_subview(self.name, [0], builder)
        i0 = _index_const(builder, 0)
        op = LoadOp.get(index, [i0])
        builder.insert(op)
        return op.results

    def codegenSet(
        self, value: SSAValue, builder: Builder
    ) -> SSAValues[OpResult[Attribute]]:
        # TODO: typer l'alloca explicitement plutôt que depuis value.type.

        if self.name not in variablesHeap:
            alloca = AllocaOp.get(value.type, shape=[1])
            builder.insert(alloca)
            variablesHeap[self.name] = alloca.memref

        index = _get_subview(self.name, [0], builder)
        i0 = _index_const(builder, 0)
        store = StoreOp.get(value, index, [i0])
        builder.insert(store)

        return store.results
