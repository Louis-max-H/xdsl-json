from __future__ import annotations

from typing import Annotated

from pydantic import Field

from xdsljson.structs import ConstFOp
from xdsljson.structs.op_binary import BinaryOp
from xdsljson.structs.op_binaryF import BinaryFOp
from xdsljson.structs.op_constant import ConstOp

# Union discriminé de toutes les opérations connues.
BaseOp = Annotated[
    BinaryOp | ConstOp | ConstFOp | BinaryFOp, Field(discriminator="type")
]

# Résout les références avant validation (utilisé par TypeAdapter(BaseOp)).
BinaryOp.model_rebuild(
    _types_namespace={
        "BaseOp": BaseOp,
        "BinaryOp": BinaryOp,
        "ConstOp": ConstOp,
        "ConstFOp": ConstFOp,
        "BinaryFOp": BinaryFOp,
    }
)
ConstOp.model_rebuild()
