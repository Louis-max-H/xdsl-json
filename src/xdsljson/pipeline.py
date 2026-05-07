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

# ────── Compile / link via shared object ────────────────────────
def compile_llvm_to_object(input_path: Path, output_path: Path) -> None:
    """Compile un fichier LLVM IR (``.ll``) en objet PIC (``.o``).

    Utilise ``llc -filetype=obj -relocation-model=pic`` afin que l'objet
    puisse ensuite être inséré dans un shared object.
    """
    llc = require_command("llc")
    llc_cmd = [
        llc,
        "-filetype=obj",
        "-relocation-model=pic",
        str(input_path),
        "-o", str(output_path),
    ]
    run_command(llc_cmd, "llc")


def build_shared_library(object_path: Path, library_path: Path) -> None:
    """Construit un shared object (``.so``) à partir d'un objet PIC.

    Les symboles externes non résolus dans ``object_path`` (par exemple
    ``print_int``) sont attendus dans le binaire qui chargera la lib :
    voir ``link_executable`` qui passe ``-rdynamic`` pour les exporter.
    """
    clangxx = require_command("clang++")
    cmd = [
        clangxx, "-shared", "-fPIC",
        str(object_path),
        "-o", str(library_path),
    ]
    run_command(cmd, "clang++")


def link_executable(
    call_source: Path,
    library_path: Path,
    output_path: Path,
) -> None:
    """Linke ``call_source`` (C++) avec ``library_path`` pour produire un exécutable.

    Utilise ``-L<dir> -l<name>`` ainsi qu'un ``rpath`` ``$ORIGIN`` pour que
    l'exécutable retrouve la lib partagée dans son propre dossier au runtime.

    ``-rdynamic`` exporte les symboles du binaire dans la table dynamique :
    indispensable pour que les symboles définis dans ``call_source`` (par
    ex. ``print_int``) puissent être résolus depuis ``library_path``.
    """
    clangxx = require_command("clang++")

    lib_dir = library_path.parent.resolve()
    lib_stem = library_path.stem
    if not lib_stem.startswith("lib"):
        raise ValueError(
            f"Le nom du shared object doit commencer par 'lib' : {library_path.name}"
        )
    lib_name = lib_stem[len("lib"):]

    cmd = [
        clangxx,
        str(call_source),
        f"-L{lib_dir}",
        f"-l{lib_name}",
        "-Wl,-rpath,$ORIGIN",
        "-rdynamic",
        "-o", str(output_path),
    ]
    run_command(cmd, "clang++")


def convert_to_executable(
    llvm_path: Path,
    call_source: Path,
    output_path: Path,
) -> Path:
    """Pipeline complète : ``.ll`` → ``.o`` → ``lib<name>.so`` → exécutable.

    - ``llvm_path`` : fichier LLVM IR généré (``somme.ll``).
    - ``call_source`` : fichier C++ qui appelle ``xdsl_main`` (``somme.call.cpp``).
    - ``output_path`` : chemin de l'exécutable final (``somme.out``).

    Retourne le chemin du shared object construit.
    """
    object_path = llvm_path.with_suffix(".o")
    library_path = llvm_path.parent / f"lib{llvm_path.stem}.so"

    compile_llvm_to_object(llvm_path, object_path)
    build_shared_library(object_path, library_path)

    if not call_source.is_file():
        print(
            f"Erreur : fichier d'appel introuvable : {call_source}\n"
            f"Crée-le (par exemple {call_source.name}) pour appeler xdsl_main\n"
            f"et y définir les symboles externes attendus (ex. print_int).",
            file=sys.stderr,
        )
        sys.exit(1)

    link_executable(call_source, library_path, output_path)
    return library_path
