"""Grammaire JSON des opérations et registre des structs LLVM.

Les opérations s'importent depuis les sous-modules (ex. ``xdsljson.structs.op_binary``).

``struct_table`` et ``struct_fields`` sont remplis par ``define struct`` et lus par
``TypeStruct`` (``xdsljson.types_interface.type_struct``).
"""

from __future__ import annotations

from xdsl.dialects.llvm import LLVMStructType

from .codegen import Typed

struct_table: dict[str, LLVMStructType] = {}
struct_fields: dict[str, dict[str, tuple[Typed, int]]] = {}

__all__ = ["struct_fields", "struct_table"]
