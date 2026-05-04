from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class ConstFOp(BaseModel):
    """Constant value operand."""

    type: Literal["constF"] = "constF"
    val: float
    size: int
