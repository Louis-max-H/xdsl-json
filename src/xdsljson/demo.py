from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter

Node = Annotated["Type1 | Type2", Field(discriminator="nodetype")] | str


class Type1(BaseModel):
    nodetype: Literal["type1"]
    thing1: int


class Type2(BaseModel):
    nodetype: Literal["type2"]
    thing2: float
    child: Node


class SomewhatRecursiveModel(BaseModel):
    root: Node


adapter: TypeAdapter[Node] = TypeAdapter(Node)
parsed_node: Node = adapter.validate_python(
    {
        "nodetype": "type2",
        "thing2": 0.3,
        "child": {"nodetype": "type1", "thing1": 1},
    }
)
print(parsed_node)
