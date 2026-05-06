#!/usr/bin/env python3
"""Point d'entrée du compilateur xDSL-JSON."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter
from xdsl.builder import Builder
from xdsl.context import Context
from xdsl.dialects import arith, builtin, scf
from xdsl.dialects.builtin import (
    ModuleOp,
)
from xdsl.interpreter import Interpreter
from xdsl.interpreters import register_implementations
from xdsl.rewriter import InsertPoint

from xdsljson.structs.base import BaseValue
from xdsljson.structs.op_function import FunctionOp


# ────── Json to AST ────────────────────────
def build_sample_ast_json(data: Any) -> FunctionOp:
    """Valide les données d'entrée et construit l'AST associé."""

    adapter: TypeAdapter[FunctionOp] = TypeAdapter(BaseValue | FunctionOp)
    return adapter.validate_python(data)


# ────── Init module ────────────────────────
def get_builder() -> tuple[ModuleOp, Builder]:
    module = ModuleOp([])
    builder = Builder(InsertPoint.at_end(module.body.block))
    return module, builder

def run_module(module: ModuleOp):
    ctx = Context()
    ctx.load_dialect(arith.Arith)
    ctx.load_dialect(builtin.Builtin)
    ctx.load_dialect(scf.Scf)
    interpreter = Interpreter(module)
    register_implementations(interpreter, ctx)

    op = interpreter.get_op_for_symbol("main")
    print("Result:\n")
    print(interpreter.call_op(op, (12, 13)))
