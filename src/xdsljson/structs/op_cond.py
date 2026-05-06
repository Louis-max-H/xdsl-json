from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from xdsl.builder import Builder
from xdsl.dialects.scf import IfOp
from xdsl.ir import SSAValue

from xdsljson.structs.block import codegenBlock
from xdsljson.structs.codegen import CodegenOp

if TYPE_CHECKING:
    from xdsljson.structs.base import BaseOp


class CondOp(CodegenOp):
    type: Literal["if"] = "if"
    cond: BaseOp
    thenBlock: list[BaseOp]
    elseBlock: list[BaseOp] | None = None

    def codegen(self, builder: Builder) -> SSAValue:
        cond_ssa = self.cond.codegen(builder)

        # Région then : on construit son bloc avec un Builder dédié.
        then_block = codegenBlock(self.thenBlock, builder)
        else_block = codegenBlock(self.elseBlock, builder)

        yield_op = then_block.last_op
        assert yield_op is not None
        return_types = [v.type for v in yield_op.operands]

        if_op = IfOp(
            cond_ssa,
            return_types,
            [then_block],
            [else_block],
        )
        builder.insert(if_op)
        return if_op.results[0]
