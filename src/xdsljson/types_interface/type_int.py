from __future__ import annotations

from enum import Enum

from xdsl.ir import Attribute
from xdsl.parser import (
    IntegerType,
    Signedness,
)

from xdsljson.structs.codegen import ABCEnumMeta, Typed


class TypeInt(Typed, Enum, metaclass=ABCEnumMeta):
    i64 = "i64"
    i32 = "i32"
    i16 = "i16"
    i8 = "i8"
    i1 = "i1"
    I64 = "I64"
    I32 = "I32"
    I16 = "I16"
    I8 = "I8"
    I1 = "I1"

    def get_type(self) -> Attribute:
        match self:
            case TypeInt.i64:
                return IntegerType(64)
            case TypeInt.i32:
                return IntegerType(32)
            case TypeInt.i16:
                return IntegerType(16)
            case TypeInt.i8:
                return IntegerType(8)
            case TypeInt.i1:
                return IntegerType(1)
            case TypeInt.I64:
                return IntegerType(64, Signedness.SIGNLESS)
            case TypeInt.I32:
                return IntegerType(32, Signedness.SIGNLESS)
            case TypeInt.I16:
                return IntegerType(16, Signedness.SIGNLESS)
            case TypeInt.I8:
                return IntegerType(8, Signedness.SIGNLESS)
            case TypeInt.I1:
                return IntegerType(1, Signedness.SIGNLESS)

    def get_attribute(self, index: str) -> tuple[Typed, int]:
        raise NotImplementedError("Int dont have attribute")
