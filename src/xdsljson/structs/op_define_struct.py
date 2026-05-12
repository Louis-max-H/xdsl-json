from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from xdsl.builder import Builder
from xdsl.dialects.llvm import LLVMStructType
from xdsl.ir import Attribute, OpResult, SSAValues

from xdsljson.structs.codegen import Codegen, Typed
from xdsljson.structs.type_basic import TypeBasic

struct_table: dict[str, LLVMStructType] = {}
struct_fields: dict[str, dict[str, tuple[Typed, int]]] = {}
# struct_field_names[struct] = {field name: (index, type)}

if TYPE_CHECKING:
    from xdsljson.structs.type_struct import TypeStruct

class DefineStructOp(Codegen):
    type: Literal["struct"] = "struct"
    name: str
    args: list[tuple[TypeBasic | TypeStruct, str]]

    # TODO: Need to insert it with builder ?
    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        # Not already defined
        assert self.name not in struct_table.keys()

        # Codegen attribute of typeds
        assert self.args is not None
        types = [
            typed.get_type()
            for (typed, _typed_name) in self.args
        ]

        # Structure
        struct = LLVMStructType.from_type_list(types)
        struct_table[self.name] = struct

        # Fields
        struct_fields[self.name] = {}
        for i, (typed, typed_name) in enumerate(self.args):
            struct_fields[self.name][typed_name] = (typed, i)

        # No code generated
        return SSAValues([])
