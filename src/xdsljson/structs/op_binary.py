from typing import Literal

from xdsljson.structs.op_operator import OperatorOp
from pydantic import BaseModel

class BinaryOp(BaseModel):
    """Binary operation composed of two operands."""

    type: Literal["binary"] = "binary"
    lhs: BaseModel
    rhs: BaseModel
    op: OperatorOp
