from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field
from xdsl.builder import Builder
from xdsl.ir import Attribute, OpResult, SSAValues

from xdsljson.structs.codegen import Codegen
from xdsljson.structs.op_define_struct import DefineStructOp
from xdsljson.structs.op_function import FunctionOp

# Définition de struct ou de function
ModuleStatement = Annotated[DefineStructOp | FunctionOp, Field(discriminator="type")]


class ModuleJsonOp(Codegen):
    """Racine JSON de type module : enregistre les structs puis génère les fonctions."""

    op: Literal["module"] = "module"
    body: list[ModuleStatement]

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        for item in self.body:
            item.codegen(builder)
        return SSAValues([])
