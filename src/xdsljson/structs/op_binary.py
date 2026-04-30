from typing import Literal

from xdsljson.structs.block import BaseBlock
from xdsljson.structs.op_operator import OperatorOp


class BinaryOp(BaseBlock):
    """Binary operation composed of two operands."""

    type: Literal["binary"] = "binary"
    lhs: BaseBlock
    rhs: BaseBlock
    op: OperatorOp
