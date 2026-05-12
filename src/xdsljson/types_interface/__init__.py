"""Types JSON scalaires (float, int) et structs pour le schéma Pydantic."""

from typing import TypeAlias

from xdsljson.types_interface.type_float import TypeFloat
from xdsljson.types_interface.type_int import TypeInt
from xdsljson.types_interface.type_struct import TypeStruct

AnyValueType: TypeAlias = TypeFloat | TypeInt | TypeStruct

__all__ = [
    "AnyValueType",
    "TypeFloat",
    "TypeInt",
    "TypeStruct",
]
