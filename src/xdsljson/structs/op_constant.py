from __future__ import annotations

from typing import Literal

from xdsljson.structs.block import BaseBlock


class ConstOp(BaseBlock):
    """Constant value operand."""

    type: Literal["const"] = "const"
    val: float | int
    size: int
