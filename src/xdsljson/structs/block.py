from __future__ import annotations

from typing import TYPE_CHECKING

from xdsl.builder import Builder
from xdsl.dialects.arith import ConstantOp
from xdsl.dialects.builtin import IntegerAttr, IntegerType
from xdsl.dialects.scf import YieldOp
from xdsl.ir import Block
from xdsl.rewriter import InsertPoint

if TYPE_CHECKING:
    from xdsljson.structs.base import BaseOp

def codegenBlock(content: list[BaseOp] | None, builder: Builder):
    # Map None block to empty block
    if content is None:
        content = []

    # Create new block
    block_ir = Block()
    block_builder = Builder(InsertPoint.at_end(block_ir))

    # Gen all elements
    last_result = None
    for element in content:
        last_result = element.codegen(block_builder)

    # Return last result
    if last_result is None:
        last_result = ConstantOp(IntegerAttr(0, IntegerType(1)))

    block_builder.insert(YieldOp(last_result))
    return block_ir
