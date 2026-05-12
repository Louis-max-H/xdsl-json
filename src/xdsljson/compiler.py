#!/usr/bin/env python3
"""Point d'entrée du compilateur xDSL-JSON."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter
from xdsl.builder import Builder
from xdsl.context import Context
from xdsl.dialects import arith, builtin, memref, scf
from xdsl.dialects.builtin import (
    IntegerType,
    ModuleOp,
)
from xdsl.dialects.func import FuncOp
from xdsl.interpreter import Interpreter
from xdsl.interpreters import register_implementations
from xdsl.ir import Region
from xdsl.rewriter import InsertPoint

from xdsljson.structs.op_function import FunctionOp
from xdsljson.structs.op_module import ModuleJsonOp
from xdsljson.structs.op_print import PRINT_INT_SYMBOL


# ────── Json to AST ────────────────────────
def build_sample_ast_json(data: Any) -> ModuleJsonOp | FunctionOp:
    """Valide les données d'entrée et construit l'AST associé."""

    adapter: TypeAdapter[ModuleJsonOp] = TypeAdapter(ModuleJsonOp)
    return adapter.validate_python(data)


# ────── Init module ────────────────────────
def declare_runtime(builder: Builder) -> None:
    """Déclare les fonctions externes fournies par le runtime C.

    Pour l'instant, seul ``print_int(i64)`` est exposé. La fonction est
    déclarée en visibilité ``private`` avec une région vide afin que MLIR
    la traite comme une déclaration externe à résoudre au link.
    """
    print_int = FuncOp(
        PRINT_INT_SYMBOL,
        ([IntegerType(64)], []),
        Region(),
        "private",
    )
    builder.insert(print_int)


def get_builder() -> tuple[ModuleOp, Builder]:
    module = ModuleOp([])
    builder = Builder(InsertPoint.at_end(module.body.block))
    declare_runtime(builder)
    return module, builder

def run_module(module: ModuleOp):
    ctx = Context()
    ctx.load_dialect(arith.Arith)
    ctx.load_dialect(builtin.Builtin)
    ctx.load_dialect(scf.Scf)
    ctx.load_dialect(memref.MemRef)
    interpreter = Interpreter(module)
    register_implementations(interpreter, ctx)

    op = interpreter.get_op_for_symbol("main")
    # print(f"main(12, 13) = {interpreter.call_op(op, (12, 13))}")
    print(f"main(10) = {interpreter.call_op(op, (10,))}")

