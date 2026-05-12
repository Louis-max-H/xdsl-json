from __future__ import annotations

from enum import Enum

from xdsl.ir import Attribute
from xdsl.parser import (
    Float16Type,
    Float32Type,
    Float64Type,
    Float80Type,
    Float128Type,
    IntegerType,
    Signedness,
)

from xdsljson.structs.codegen import ABCEnumMeta, Typed


class TypeBasic(Typed, Enum, metaclass=ABCEnumMeta):
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
    f16 = "f16"
    f32 = "f32"
    f64 = "f64"
    f80 = "f80"
    f128 = "f128"

    def get_type(self) -> Attribute:
        match self:
            case TypeBasic.i64:
                return IntegerType(64)
            case TypeBasic.i32:
                return IntegerType(32)
            case TypeBasic.i16:
                return IntegerType(16)
            case TypeBasic.i8:
                return IntegerType(8)
            case TypeBasic.i1:
                return IntegerType(8)
            case TypeBasic.I64:
                return IntegerType(64, Signedness.SIGNLESS)
            case TypeBasic.I32:
                return IntegerType(32, Signedness.SIGNLESS)
            case TypeBasic.I16:
                return IntegerType(16, Signedness.SIGNLESS)
            case TypeBasic.I8:
                return IntegerType(8, Signedness.SIGNLESS)
            case TypeBasic.I1:
                return IntegerType(1, Signedness.SIGNLESS)
            case TypeBasic.f16:
                return Float16Type()
            case TypeBasic.f32:
                return Float32Type()
            case TypeBasic.f64:
                return Float64Type()
            case TypeBasic.f80:
                return Float80Type()
            case TypeBasic.f128:
                return Float128Type()

    def index_of(self, index: str) -> tuple[Typed, int]:
        raise NotImplementedError("Basic type can't be indexed")
