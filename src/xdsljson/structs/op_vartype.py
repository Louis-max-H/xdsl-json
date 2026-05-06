from enum import Enum

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

    def codegen(self) -> IntegerType | AnyFloat:
        match self.value:
            case "i64":
                return IntegerType(64)
            case "i32":
                return IntegerType(32)
            case "i16":
                return IntegerType(16)
            case "i8":
                return IntegerType(8)
            case "i1":
                return IntegerType(8)
            case "I64":
                return IntegerType(64, Signedness.SIGNLESS)
            case "I32":
                return IntegerType(32, Signedness.SIGNLESS)
            case "I16":
                return IntegerType(16, Signedness.SIGNLESS)
            case "I8":
                return IntegerType(8, Signedness.SIGNLESS)
            case "I1":
                return IntegerType(1, Signedness.SIGNLESS)
            case "f16":
                return Float16Type()
            case "f32":
                return Float32Type()
            case "f64":
                return Float64Type()
            case "f80":
                return Float80Type()
            case "f128":
                return Float128Type()


