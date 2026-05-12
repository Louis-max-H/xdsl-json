from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from xdsl.builder import Builder
from xdsl.dialects.func import CallOp
from xdsl.ir import Attribute, OpResult, SSAValues

from xdsljson.structs.codegen import Codegen

if TYPE_CHECKING:
    from xdsljson.structs.base import BaseValue


# Nom de la fonction externe (fournie par le code d'appel C++) qui imprime un entier.
PRINT_INT_SYMBOL = "print_int"


class PrintOp(Codegen):
    """Affiche la valeur d'une expression via la fonction externe ``print_int``.

    La déclaration ``func.func private @print_int(i64) -> ()`` est ajoutée
    automatiquement au module par ``compiler.declare_runtime``. Le symbole
    doit être défini dans le fichier d'appel C++ associé (par exemple
    ``examples/somme.call.cpp``) avec un linkage ``extern "C"`` ; il est
    résolu une fois pour toutes au link statique entre le ``.o`` issu du
    pipeline xDSL et l'objet du fichier d'appel.
    """

    type: Literal["print"] = "print"
    value: BaseValue

    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        value_ssa = self.value.codegen(builder)
        if len(value_ssa) != 1:
            raise ValueError(
                f"print attend une seule SSAValue, en a reçu {len(value_ssa)}"
            )

        call = CallOp(PRINT_INT_SYMBOL, [value_ssa[0]], [])
        builder.insert(call)
        return call.results
