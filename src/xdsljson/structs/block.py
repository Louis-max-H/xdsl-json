from __future__ import annotations

from typing import TYPE_CHECKING

from xdsl.builder import Builder
from xdsl.ir import Attribute, Block, OpResult, SSAValues
from xdsl.rewriter import InsertPoint

if TYPE_CHECKING:
    from xdsljson.structs.base import BaseValue

def codegenBlock(
    content: list[BaseValue] | None,
    block: Block,
) -> tuple[Block, SSAValues[OpResult[Attribute]] | None]:
    # Map None block to empty block
    if content is None:
        content = []

    # Build into the provided block (caller decides whether it's a fresh
    # Block() or an existing one such as a FuncOp entry block).
    block_builder = Builder(InsertPoint.at_end(block))
    # TODO: On renvoie automatiquement la dernière valeur, mais utiliser plutôt yield

    last_value = None
    for element in content:
        last_value = element.codegen(block_builder)

    return block, last_value
