#!/usr/bin/env python3
"""Point d'entrée du compilateur xDSL-JSON."""

from __future__ import annotations

import argparse
import json as json_lib
import sys
from pathlib import Path
from typing import Any

import yaml

from xdsljson.compiler import build_sample_ast_json, get_builder
from xdsljson.pipeline import (
    convert_to_executable,
    convert_to_llvm,
    run_mlir_opt,
    xdsl_to_mlir,
)
from xdsljson.utils import print_two_columns

MLIR_OPT_PASSES = [
    "--mem2reg",
    "--expand-strided-metadata",
    "--normalize-memrefs",
    "--memref-expand",
    "--fold-memref-alias-ops",
    "--canonicalize"
]

LOWER_TO_LLVM = [
    "--reconcile-unrealized-casts",
    "--convert-scf-to-cf",
    "--convert-cf-to-llvm",
    "--convert-func-to-llvm",
    "--finalize-memref-to-llvm",
    "--convert-arith-to-llvm",
    "--canonicalize"
]

def load_input_file(path: Path) -> Any:
    """Charge un fichier JSON ou YAML et renvoie le dictionnaire correspondant.

    Le YAML est converti en dictionnaire Python (équivalent JSON) avant validation.
    """
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")

    if suffix == ".json":
        return json_lib.loads(text)
    if suffix in (".yaml", ".yml"):
        return yaml.safe_load(text)
    raise ValueError(
        f"Extension de fichier non supportée : {suffix!r}. "
        "Utilisez .json, .yaml ou .yml."
    )

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse les arguments en ligne de commande."""
    parser = argparse.ArgumentParser(
        prog="xdsljson",
        description=(
            "Compile une description JSON/YAML en IR xDSL puis l'exécute "
            "via l'interpréteur."
        ),
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Chemin vers le fichier d'entrée (.json, .yaml ou .yml).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # ────── Read files
    input_path: Path = args.input
    print(f"Lecture de {input_path}")
    if not input_path.is_file():
        print(f"Erreur : fichier introuvable : {input_path}", file=sys.stderr)
        return 1

    try:
        data = load_input_file(input_path)
    except (ValueError, OSError, json_lib.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"Erreur lors du chargement de {input_path} : {exc}", file=sys.stderr)
        return 1

    # ────── Gen AST
    print("Ast using python class")
    function_ast = build_sample_ast_json(data)
    print(function_ast.model_dump())
    print("\n")

    # ────── Convert to xDSL
    module, builder = get_builder()
    function_ast.codegen(builder)
    module.verify()

    # ────── xDSL to MLIR
    file_mlir = input_path.with_suffix(".mlir")
    file_optimized = input_path.with_suffix(".mlir.opt")
    file_llvm_mlir = input_path.with_suffix(".llvm.mlir")
    file_llvm = input_path.with_suffix(".ll")
    file_runnable = input_path.with_suffix(".out")

    # ────── xDSL to MLIR
    mlir_str = xdsl_to_mlir(module, file_mlir)

    # ────── Optimize MLIR
    optimized_str = run_mlir_opt(file_mlir, file_optimized, MLIR_OPT_PASSES)
    print_two_columns(
        "───────── Raw MLIR ─────────\n" + mlir_str,
        "────── Optimized MLIR ──────\n" + optimized_str
    )
    print("\n")

    # ────── Lower to LLVM dialect (MLIR → MLIR @ llvm dialect)
    run_mlir_opt(file_optimized, file_llvm_mlir, LOWER_TO_LLVM)

    # ────── Translate LLVM-dialect MLIR → LLVM IR textuel (.ll)
    convert_to_llvm(file_llvm_mlir, file_llvm)

    # ────── Compile
    convert_to_executable(file_llvm, file_runnable)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
