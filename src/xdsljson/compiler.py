#!/usr/bin/env python3
"""Point d'entrée du compilateur xDSL-JSON."""

from __future__ import annotations

from xdsl.context import Context
from xdsl.dialects import arith, builtin

from xdsljson.structs.block import BaseBlock


def get_context() -> Context:
    """Construit un contexte avec les dialectes requis."""
    ctx = Context()
    ctx.load_dialect(arith.Arith)
    ctx.load_dialect(builtin.Builtin)
    return ctx


def build_sample_expression() -> BaseBlock:
    """Construit une petite expression pour démonstration."""
    raw_data = {
        "type": "binary",
        "op": "+",
        "lhs": {"type": "const", "val": 12, "size": 64},
        "rhs": {
            "type": "binary",
            "op": "*",
            "lhs": {"type": "const", "val": 13, "size": 64},
            "rhs": {"type": "const", "val": 15, "size": 64},
        },
    }
    return BaseBlock.model_validate(raw_data)


def main():
    print("Hello world!")
    expr = build_sample_expression()

    print(expr.model_dump())


if __name__ == "__main__":
    main()
