#!/usr/bin/env python3
"""Point d'entrée du compilateur xDSL-JSON."""

from __future__ import annotations

import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from xdsl.printer import Printer


# ────── Helpers ────────────────────────
def require_command(name: str) -> str:
    """Retourne le chemin absolu de ``name`` ou termine le programme."""
    path = shutil.which(name)
    if path is None:
        print(
            f"Erreur : {name} introuvable dans le PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    return path


def run_command(cmd: list[str], tool_name: str | None = None) -> str:
    """Affiche puis exécute ``cmd`` et retourne sa sortie standard.

    Si la commande échoue, écrit l'erreur sur ``stderr`` et termine le
    programme. ``tool_name`` est utilisé dans le message d'erreur
    (par défaut, le premier élément de ``cmd``).
    """
    name = tool_name or Path(cmd[0]).name
    print(shlex.join(cmd).replace(" -", "\n\t-"))

    try:
        return subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except subprocess.CalledProcessError as exc:
        print(f"Erreur lors de l'exécution de {name} :", file=sys.stderr)
        print(exc.stderr, file=sys.stderr)
        sys.exit(1)


# ────── xdsl_to_mlir ────────────────────────
def xdsl_to_mlir(module: Any, output_path: Path) -> str:
    # Writte to file
    with output_path.open("w", encoding="utf-8") as f:
        Printer(stream=f).print_op(module)
        f.write("\n")

    # Return content
    with output_path.open("r", encoding="utf-8") as f:
        return f.read()

# ────── MLIR opt ────────────────────────
def run_mlir_opt(
    input_path: Path,
    output_path: Path,
    passes: list[str]
) -> str:
    # Find mlir_opt
    mlir_opt = require_command("mlir-opt")

    # Gen command and run
    mlir_opt_cmd = [mlir_opt, *passes, str(input_path)]
    opt_result = run_command(mlir_opt_cmd, "mlir-opt")

    # Writte to file
    with output_path.open("w", encoding="utf-8") as f:
        f.write(opt_result)

    print("{}: {} lines\n".format(output_path.name, opt_result.count("\n")))
    return opt_result


# ────── Lower to LLVM ────────────────────────
def convert_to_llvm(input_path: Path, output_path: Path) -> str:
    mlir_translate = require_command("mlir-translate")

    mlir_translate_cmd = [
        mlir_translate, "--mlir-to-llvmir",
        str(input_path),
    ]
    llvm_result = run_command(mlir_translate_cmd, "mlir-translate")

    # Writte to file
    with output_path.open("w", encoding="utf-8") as f:
        f.write(llvm_result)

    print("{}: {} lines\n".format(output_path.name, llvm_result.count("\n")))
    return llvm_result

# ────── Lower to LLVM ────────────────────────
# Chemin vers le runtime C (fournit notamment ``print_int``).
RUNTIME_C = Path(__file__).resolve().parents[2] / "runtime" / "runtime.c"


def convert_to_executable(input_path: Path, output_path: Path):
    llc = require_command("llc")
    clang = require_command("clang")

    # Convert to text assembly
    s_file = str(output_path.with_suffix(".s"))
    llc_cmd = [llc, str(input_path), "-o", s_file]
    run_command(llc_cmd, "llc")

    # Link to executable (avec le runtime C s'il est disponible).
    clang_cmd = [clang, s_file]
    if RUNTIME_C.is_file():
        clang_cmd.append(str(RUNTIME_C))
    clang_cmd.extend(["-o", str(output_path)])
    run_command(clang_cmd, "clang")
