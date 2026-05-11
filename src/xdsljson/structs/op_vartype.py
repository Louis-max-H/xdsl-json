from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from xdsl.dialects.builtin import ArrayAttr, StringAttr
from xdsl.dialects.llvm import LLVMStructType
from xdsl.ir import Attribute
from xdsl.parser import (
    AnyFloat,
    Float16Type,
    Float32Type,
    Float64Type,
    Float80Type,
    Float128Type,
    IntegerType,
    Signedness,
)

if TYPE_CHECKING:
    from xdsljson.structs.op_var import VarOp

struct_table: dict[str, LLVMStructType] = {}


def define_struct(name: str, args: list[VarOp]):
    # create arg_types
    arg_types: list[Attribute] = []
    for arg in args:
        if arg.varType is None:
            raise ValueError("Type is mendatory for struct definition")
        arg_types.append(vartype_codegen(arg.varType))

    # create structtion
    struct_table[name] = LLVMStructType(StringAttr(name), ArrayAttr(arg_types))


def get_struct(name: str) -> LLVMStructType:
    if name not in struct_table:
        raise KeyError(
            f"Unknown struct type {name!r}; register it with define_struct first"
        )
    return struct_table[name]


class VarTypeOp(Enum):
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

    def codegen(self) -> AnyFloat | IntegerType:
        match self:
            case VarTypeOp.i64:
                return IntegerType(64)
            case VarTypeOp.i32:
                return IntegerType(32)
            case VarTypeOp.i16:
                return IntegerType(16)
            case VarTypeOp.i8:
                return IntegerType(8)
            case VarTypeOp.i1:
                return IntegerType(8)
            case VarTypeOp.I64:
                return IntegerType(64, Signedness.SIGNLESS)
            case VarTypeOp.I32:
                return IntegerType(32, Signedness.SIGNLESS)
            case VarTypeOp.I16:
                return IntegerType(16, Signedness.SIGNLESS)
            case VarTypeOp.I8:
                return IntegerType(8, Signedness.SIGNLESS)
            case VarTypeOp.I1:
                return IntegerType(1, Signedness.SIGNLESS)
            case VarTypeOp.f16:
                return Float16Type()
            case VarTypeOp.f32:
                return Float32Type()
            case VarTypeOp.f64:
                return Float64Type()
            case VarTypeOp.f80:
                return Float80Type()
            case VarTypeOp.f128:
                return Float128Type()


# Chaîne qui n'est pas un membre de VarTypeOp = nom de struct (struct_table).
VarType = VarTypeOp | str

def vartype_codegen(v: VarTypeOp | str) -> AnyFloat | IntegerType | LLVMStructType:
    if isinstance(v, str):
        return get_struct(v)
    return v.codegen()
