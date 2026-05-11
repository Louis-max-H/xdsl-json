from __future__ import annotations

from typing import Literal

from xdsl.builder import Builder
from xdsl.dialects.llvm import LLVMStructType
from xdsl.ir import Attribute, OpResult, SSAValues

from xdsljson.structs.codegen import CodegenResult
from xdsljson.structs.op_var import VarOp
from xdsljson.structs.op_vartype import define_struct

struct_table: dict[str, LLVMStructType] = {}

class StructOp(CodegenResult):
    type: Literal["struct"] = "struct"
    name: str
    args: list[VarOp]

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        # Add struct to struc_table
        define_struct(self.name, self.args)

        # No code generated
        return SSAValues([])
