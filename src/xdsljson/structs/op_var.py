from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, NamedTuple

from pydantic import ConfigDict
from xdsl.builder import Builder
from xdsl.dialects.arith import ConstantOp
from xdsl.dialects.builtin import IndexType, MemRefType
from xdsl.dialects.memref import AllocaOp, LoadOp, StoreOp
from xdsl.ir import Attribute, OpResult, SSAValue, SSAValues

from xdsljson.structs.codegen import Codegen
from xdsljson.types_interface.any_value_type import AnyValueType


class VarInstance(NamedTuple):
    type: AnyValueType  # Python type
    add: OpResult[MemRefType[Attribute]]  # Allocation addresse


variables_heap: dict[str, VarInstance] = {}


# TODO: instanciate only once at top function
# TODO: Clear variable end of function
def _index(n: int, builder: Builder) -> SSAValue:
    op = ConstantOp.from_int_and_width(n, IndexType())
    builder.insert(op)
    return op.result


class VarOp(Codegen):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    op: Literal["var"] = "var"
    name: str
    type: AnyValueType | None = None

    def get_name(self) -> str:
        return self.name.split(".")[0]

    def get_address(self) -> OpResult[MemRefType[Attribute]]:
        return variables_heap[self.get_name()].add

    def get_memref_base_type(self) -> MemRefType[Attribute]:
        return variables_heap[self.get_name()].add.type

    def get_python_base_type(self) -> AnyValueType:
        # Load type
        given_type = self.type
        if self.get_name() in variables_heap.keys():
            saved_type = variables_heap[self.get_name()].type
        else:
            saved_type = None

        # Check types
        match (given_type is None, saved_type is None):
            case (True, True):
                raise Exception(f"Can't find type for {repr(self.name)}")
            case (True, False):
                return saved_type  # pyright: ignore[reportReturnType]
            case (False, True):
                return given_type  # pyright: ignore[reportReturnType]
            case (False, False):
                assert type(saved_type) is type(given_type)
                return saved_type  # pyright: ignore[reportReturnType]

    def get_indices_str(self) -> Sequence[str]:
        return self.name.split(".")[1::]

    def get_indices(self, builder: Builder) -> Sequence[SSAValue]:
        base_type = self.get_python_base_type()
        index = [_index(0, builder)]

        for attribute in self.get_indices_str():
            attribute_type, attribute_index = base_type.get_attribute(attribute)
            base_type = attribute_type
            index.append(_index(attribute_index, builder))

        return index

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        if self.get_name() not in variables_heap:
            raise ValueError(f"{self.get_name()} not found in variable heap")

        addr = self.get_address()
        indices = self.get_indices(builder)
        print("LoadOp:")
        print(f"addr dim    : {addr.type.get_num_dims()}")
        print(f"      shape : {addr.type.shape.data}")
        print(f"indices dim : {len(indices)}")
        print(f"       shape: {indices}")
        print()
        op = LoadOp.get(addr, indices)

        builder.insert(op)
        return op.results

    def codegenSet(
        self, value: SSAValue, builder: Builder
    ) -> SSAValues[OpResult[Attribute]]:

        # Allocate
        if self.get_name() not in variables_heap:
            alloca = AllocaOp.get(value.type, shape=[1])
            builder.insert(alloca)
            variables_heap[self.get_name()] = VarInstance(
                self.get_python_base_type(), alloca.memref
            )

        # Set value
        addr = self.get_address()
        indices = self.get_indices(builder)
        print("StoreOp:")
        print(f"addr dim    : {addr.type.get_num_dims()}")
        print(f"      shape : {addr.type.shape.data}")
        print(f"indices dim : {len(indices)}")
        print(f"       shape: {indices}")
        print()

        store = StoreOp.get(value, addr, indices)
        builder.insert(store)

        return store.results
