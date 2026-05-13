from __future__ import annotations

from typing import Literal

from xdsl.builder import Builder
from xdsl.dialects.builtin import ArrayAttr, StringAttr
from xdsl.dialects.llvm import LLVMStructType
from xdsl.ir import Attribute, OpResult, SSAValues

from xdsljson.structs import struct_fields, struct_table
from xdsljson.structs.codegen import Codegen
from xdsljson.types_interface.any_value_type import AnyValueType


class DefineStructOp(Codegen):
    op: Literal["define struct"] = "define struct"
    name: str
    args: list[tuple[AnyValueType, str]]

    # TODO: Need to insert it with builder ?
    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        # Not already defined
        assert self.name not in struct_table.keys()

        # Codegen attribute of typeds
        assert self.args is not None
        types = [typed.get_type() for (typed, _typed_name) in self.args]

        # Structure
        struct = LLVMStructType(
            StringAttr(self.name),
            ArrayAttr(types),
        )
        struct_table[self.name] = struct

        # Fields
        struct_fields[self.name] = {}
        for i, (typed, typed_name) in enumerate(self.args):
            struct_fields[self.name][typed_name] = (typed, i)

        # No code generated
        return SSAValues([])
