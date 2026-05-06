from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict
from xdsl.builder import Builder
from xdsl.ir import Attribute, OpResult, SSAValue, SSAValues


# ABC : Abstract Base Class
class CodegenValue(BaseModel, ABC):
    """Mixin fournissant la signature commune de génération."""

    # Necessaire pour autoriser les classes externes (xDSL: Builder)
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    model_config = ConfigDict()

    # Force les sous-classes à implémenter cette méthode abstraite
    @abstractmethod
    def codegen(self, builder: Builder) -> SSAValue:
        """Génère l'opération xDSL et retourne la SSA produite.
        """
        raise NotImplementedError

class CodegenResult(BaseModel, ABC):
    model_config = ConfigDict()

    @abstractmethod
    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        raise NotImplementedError
