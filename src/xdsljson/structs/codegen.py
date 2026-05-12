from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from enum import EnumMeta

from pydantic import BaseModel, ConfigDict
from xdsl.builder import Builder
from xdsl.ir import Attribute, OpResult, SSAValues


# ABC : Abstract Base Class
class Codegen(BaseModel, ABC):

    # Necessaire pour autoriser les classes externes (xDSL: Builder)
    # model_config = ConfigDict(arbitrary_types_allowed=True)
    model_config = ConfigDict()

    # Force les sous-classes à implémenter cette méthode abstraite
    @abstractmethod
    def codegen(self, builder: Builder) -> SSAValues[OpResult[Attribute]]:
        """Génère l'opération xDSL et retourne la SSA produite.
        """
        raise NotImplementedError

# ABC : Abstract Base Class
class Typed(ABC):
    @abstractmethod
    def get_type(self) -> Attribute:
        raise NotImplementedError

    @abstractmethod
    def index_of(self, index: str) -> tuple[Typed, int]:
        raise NotImplementedError


class ABCEnumMeta(EnumMeta, ABCMeta):
    """Permet d'hériter à la fois de Enum et de Typed (ABC)."""


def sameFormat(
    lhs: SSAValues[OpResult[Attribute]] | None,
    rhs: SSAValues[OpResult[Attribute]] | None,
) -> None | tuple[SSAValues[OpResult[Attribute]], SSAValues[OpResult[Attribute]]]:
    if (
        lhs is None
        or rhs is None
        or len(lhs) != len(rhs)
    ):
        return None
    return lhs, rhs
