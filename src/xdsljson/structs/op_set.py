from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from xdsl.builder import Builder
from xdsl.ir import Attribute, OpResult, SSAValues

from xdsljson.structs.codegen import Codegen
from xdsljson.structs.op_var import VarOp
from xdsljson.types_interface.any_value_type import AnyValueType

if TYPE_CHECKING:
    from xdsljson.structs.base import BaseValue


class SetOp(Codegen):
    """Opération binaire composée de deux opérandes."""

    op: Literal["set"] = "set"
    lhs: tuple[str, AnyValueType | None]
    rhs: BaseValue

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        # Gen value
        values = self.rhs.codegen(builder)
        assert len(values) == 1

        # Gen var
        varOp = VarOp(name=self.lhs[0], type=self.lhs[1])
        return varOp.codegenSet(values[0], builder)
