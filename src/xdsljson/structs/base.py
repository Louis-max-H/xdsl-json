from __future__ import annotations

from typing import Annotated

from pydantic import Field

from xdsljson.structs.op_binary import BinaryOp
from xdsljson.structs.op_cond import CondOp
from xdsljson.structs.op_constant import ConstOp
from xdsljson.structs.op_define_struct import DefineStructOp
from xdsljson.structs.op_print import PrintOp
from xdsljson.structs.op_set import SetOp
from xdsljson.structs.op_var import VarOp
from xdsljson.structs.op_while import WhileOp
from xdsljson.types_interface.type_float import TypeFloat
from xdsljson.types_interface.type_int import TypeInt
from xdsljson.types_interface.type_struct import TypeStruct

# Union discriminé de toutes les opérations connues.
BaseValue = Annotated[
    BinaryOp | ConstOp | CondOp | VarOp | WhileOp | PrintOp | SetOp,
    Field(discriminator="op"),
]


_types_namespace = {
    "BaseValue": BaseValue,
    "BinaryOp": BinaryOp,
    "CondOp": CondOp,
    "ConstOp": ConstOp,
    "DefineStructOp": DefineStructOp,
    "PrintOp": PrintOp,
    "SetOp": SetOp,
    "VarOp": VarOp,
    "WhileOp": WhileOp,
    "TypeFloat": TypeFloat,
    "TypeInt": TypeInt,
    "TypeStruct": TypeStruct,
}

# Rebuild pydantic model because of recursive definitions
BinaryOp.model_rebuild(_types_namespace=_types_namespace)
CondOp.model_rebuild(_types_namespace=_types_namespace)
ConstOp.model_rebuild(_types_namespace=_types_namespace)
DefineStructOp.model_rebuild(_types_namespace=_types_namespace)
PrintOp.model_rebuild(_types_namespace=_types_namespace)
SetOp.model_rebuild(_types_namespace=_types_namespace)
TypeStruct.model_rebuild(_types_namespace=_types_namespace)
VarOp.model_rebuild(_types_namespace=_types_namespace)
WhileOp.model_rebuild(_types_namespace=_types_namespace)
