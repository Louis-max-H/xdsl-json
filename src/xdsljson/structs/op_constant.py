from __future__ import annotations

from typing import Literal
from pydantic import BaseModel

class ConstOp(BaseModel):
    """Constant value operand."""

    type: Literal["const"] = "const"
    val: float | int
    size: int
