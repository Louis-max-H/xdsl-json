from __future__ import annotations

from typing import Annotated

from pydantic import Field

from xdsljson.structs.op_binary import BinaryOp
from xdsljson.structs.op_cond import CondOp
from xdsljson.structs.op_constant import ConstOp
from xdsljson.structs.op_var import VarOp

# Union discriminé de toutes les opérations connues.
BaseValue = Annotated[
    BinaryOp | ConstOp | CondOp | VarOp, Field(discriminator="type")
]

_types_namespace = {
    "BaseValue": BaseValue,
    "BinaryOp": BinaryOp,
    "ConstOp": ConstOp,
    "CondOp": CondOp,
    "VarOp": VarOp,
}

# Rebuild pydantic model because of recursive definitions
BinaryOp.model_rebuild(_types_namespace=_types_namespace)
ConstOp.model_rebuild(_types_namespace=_types_namespace)
CondOp.model_rebuild(_types_namespace=_types_namespace)
VarOp.model_rebuild(_types_namespace=_types_namespace)
