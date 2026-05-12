from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from xdsl.builder import Builder
from xdsl.dialects.scf import IfOp, YieldOp
from xdsl.ir import Attribute, Block, OpResult, SSAValues

from xdsljson.structs.block import codegenBlock
from xdsljson.structs.codegen import Codegen, sameFormat

if TYPE_CHECKING:
    from xdsljson.structs.base import BaseValue


class CondOp(Codegen):
    op: Literal["if"] = "if"
    cond: BaseValue
    thenBlock: list[BaseValue]
    elseBlock: list[BaseValue] | None = None

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        # Check condition
        conds_ssa = self.cond.codegen(builder)
        assert len(conds_ssa) == 1
        cond_ssa = conds_ssa[0]

        # Région then : on construit son bloc avec un Builder dédié.
        (then_block, then_op)  = codegenBlock(self.thenBlock, Block())
        (else_block, else_op)  = codegenBlock(self.elseBlock, Block())

        # Add yield if same format
        if return_format := sameFormat(then_op, else_op):
            then_block.add_op(YieldOp(*return_format[0]))
            else_block.add_op(YieldOp(*return_format[1]))
            return_types = [v.type for v in return_format[0]]
        else:
            return_types = []

        # Create IfOp
        if_op = IfOp(
            cond_ssa,
            return_types,
            [then_block],
            [else_block],
        )
        builder.insert(if_op)
        return if_op.results
