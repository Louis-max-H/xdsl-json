from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from xdsl.ir import Attribute

from xdsljson.structs.codegen import Typed
from xdsljson.structs.op_define_struct import struct_fields, struct_table

# TODO: Array ?

class TypeStruct(BaseModel, Typed):
    model_config = ConfigDict()
    name: str

    def get_type(self) -> Attribute:
        # Struct exist
        assert self.name in struct_table.keys()
        return struct_table[self.name]

    def index_of(self, index: str) -> tuple[Typed, int]:
        assert self.name in struct_fields.keys()
        assert index in struct_fields[self.name].keys()
        return struct_fields[self.name][index]


