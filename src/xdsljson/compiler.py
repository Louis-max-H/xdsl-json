#!/usr/bin/env python3
"""Point d'entrée du compilateur xDSL-JSON."""

from __future__ import annotations

from typing import Any

from pydantic import TypeAdapter
from xdsl.builder import Builder
from xdsl.context import Context
from xdsl.dialects import arith, builtin, scf
from xdsl.dialects.builtin import (
    IntegerType,
    ModuleOp,
)
from xdsl.dialects.func import FuncOp
from xdsl.interpreter import Interpreter
from xdsl.interpreters import register_implementations
from xdsl.rewriter import InsertPoint

from xdsljson.structs.base import BaseOp


# ────── Json to AST ────────────────────────
def build_sample_ast_json(data: Any) -> BaseOp:
    """Valide les données d'entrée et construit l'AST associé."""

    adapter: TypeAdapter[BaseOp] = TypeAdapter(BaseOp)
    return adapter.validate_python(data)


# ────── Init module ────────────────────────
def get_builder() -> tuple[ModuleOp, Builder]:
    module = ModuleOp([])
    builder = Builder(InsertPoint.at_end(module.body.block))

    # Create the MLIR types for each symbol.
    arg_types = [IntegerType(64), IntegerType(64)]

    # Create a new function and inserts it inside the module.
    func = FuncOp("main", (arg_types, [IntegerType(64)]))
    builder.insert(func)

    # Associate each symbol with its MLIR name.
    arg_values = {arg: value for arg, value in zip(["a", "b"], func.args)}

    # Set the name for each function argument. This is only to get better names
    # for IR values.
    for arg, value in arg_values.items():
        value.name_hint = arg

    # Set the builder insertion point inside the function.
    builder.insertion_point = InsertPoint.at_end(func.body.block)

    # Convert the expression into MLIR IR inside the function.
    # result = emit_op(expr, builder, arg_values)
    return module, builder

    # Insert a return statement at the end of the function.
    # builder.insert(ReturnOp(result))
    # return module


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
