from __future__ import annotations

from enum import Enum

from xdsl.ir import Attribute
from xdsl.parser import (
    Float16Type,
    Float32Type,
    Float64Type,
    Float80Type,
    Float128Type,
)

from xdsljson.structs.codegen import ABCEnumMeta, Typed


class TypeFloat(Typed, Enum, metaclass=ABCEnumMeta):
    f16 = "f16"
    f32 = "f32"
    f64 = "f64"
    f80 = "f80"
    f128 = "f128"

    def get_type(self) -> Attribute:
        match self:
            case TypeFloat.f16:
                return Float16Type()
            case TypeFloat.f32:
                return Float32Type()
            case TypeFloat.f64:
                return Float64Type()
            case TypeFloat.f80:
                return Float80Type()
            case TypeFloat.f128:
                return Float128Type()

    def get_attribute(self, index: str) -> tuple[Typed, int]:
        raise NotImplementedError("Float dont have attribute")
