from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from xdsl.builder import Builder
from xdsl.dialects import scf
from xdsl.ir import Attribute, Block, OpResult, Region, SSAValues
from xdsl.rewriter import InsertPoint

from xdsljson.structs.block import codegenBlock
from xdsljson.structs.codegen import Codegen

if TYPE_CHECKING:
    from xdsljson.structs.base import BaseValue


class WhileOp(Codegen):
    type: Literal["while"] = "while"
    cond: BaseValue
    thenBlock: list[BaseValue]

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        # Before region: compute the condition and terminate with scf.condition.
        # Variables go through memref load/store, so no SSA values need to be
        # threaded through the loop.
        before_block = Block()
        before_builder = Builder(InsertPoint.at_end(before_block))
        conds_ssa = self.cond.codegen(before_builder)
        assert len(conds_ssa) == 1
        before_builder.insert(scf.ConditionOp(conds_ssa[0]))

        # After region: body + scf.yield to loop back to the before region.
        after_block, _ = codegenBlock(self.thenBlock, Block())
        after_builder = Builder(InsertPoint.at_end(after_block))
        after_builder.insert(scf.YieldOp())

        while_op = scf.WhileOp(
            [],
            [],
            Region(before_block),
            Region(after_block),
        )
        builder.insert(while_op)
        return while_op.results
