/*
 * Petit runtime C lié aux exécutables produits par xdsl-json.
 *
 * Il expose les fonctions externes que le compilateur peut appeler depuis
 * le code MLIR / LLVM IR généré. Toute nouvelle fonction « builtin » devra
 * être ajoutée ici puis déclarée côté MLIR via `declare_runtime` dans
 * `src/xdsljson/compiler.py`.
 */

#include <stdint.h>
#include <stdio.h>

void print_int(int64_t value) {
    printf("%ld\n", (long)value);
}
