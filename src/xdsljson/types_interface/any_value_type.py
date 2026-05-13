"""Alias d'union des types valeur JSON (scalaires + struct)."""

from __future__ import annotations

from typing import TypeAlias

from xdsljson.types_interface.type_float import TypeFloat
from xdsljson.types_interface.type_int import TypeInt
from xdsljson.types_interface.type_struct import TypeStruct

AnyValueType: TypeAlias = TypeFloat | TypeInt | TypeStruct
