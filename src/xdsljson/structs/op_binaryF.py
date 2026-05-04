from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel

from xdsljson.structs.op_operator import OperatorOp

if TYPE_CHECKING:
    from xdsljson.structs.op_base import BaseOp
    from xdsljson.structs.op_constantF import ConstFOp


class BinaryFOp(BaseModel):
    """Opération binaire composée de deux opérandes."""

    type: Literal["binaryF"] = "binaryF"
    lhs: BaseOp
    rhs: ConstFOp
    op: OperatorOp
