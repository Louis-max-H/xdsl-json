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

# ────── Compile / link via static linking ────────────────────────
def compile_llvm_to_object(input_path: Path, output_path: Path) -> None:
    """Compile un fichier LLVM IR (``.ll``) en objet statique (``.o``).
    Utilise ``llc -filetype=obj -relocation-model=static``
    """
    llc = require_command("llc")
    llc_cmd = [
        llc,
        "-filetype=obj",
        "-relocation-model=static",
        str(input_path),
        "-o", str(output_path),
    ]
    run_command(llc_cmd, "llc")


def link_executable(
    call_source: Path,
    object_path: Path,
    output_path: Path,
) -> None:
    """Linke ``call_source`` (C++) et ``object_path`` en un exécutable statique.

    ``-no-pie`` est requis pour rester cohérent avec un ``.o`` non-PIC :
    le binaire produit n'est pas relocalisable, mais évite l'overhead du
    PIC (registre dédié, indirection GOT/PLT). Plus besoin de ``-rdynamic``
    ni de ``rpath`` : les symboles externes (ex. ``print_int``) sont
    résolus une fois pour toutes au link, directement depuis le ``.o`` du
    fichier d'appel.
    """
    clangxx = require_command("clang++")

    cmd = [
        clangxx,
        "-no-pie",
        str(object_path),
        str(call_source),
        "-o", str(output_path),
    ]
    run_command(cmd, "clang++")


def convert_to_executable(
    llvm_path: Path,
    call_source: Path,
    output_path: Path,
) -> Path:
    """Pipeline complète : ``.ll`` → ``.o`` → exécutable statique.

    - ``llvm_path`` : fichier LLVM IR généré (``somme.ll``).
    - ``call_source`` : fichier C++ qui appelle ``xdsl_main`` (``somme.call.cpp``).
    - ``output_path`` : chemin de l'exécutable final (``somme.out``).

    Retourne le chemin de l'objet construit.
    """
    object_path = llvm_path.with_suffix(".o")

    compile_llvm_to_object(llvm_path, object_path)

    if not call_source.is_file():
        print(
            f"Erreur : fichier d'appel introuvable : {call_source}\n"
            f"Crée-le (par exemple {call_source.name}) pour appeler xdsl_main\n"
            f"et y définir les symboles externes attendus (ex. print_int).",
            file=sys.stderr,
        )
        sys.exit(1)

    link_executable(call_source, object_path, output_path)
    return object_path
