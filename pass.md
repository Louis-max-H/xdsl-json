# Analyse des passes `xdsl/transforms/`

Ce document liste les passes définies dans `xdsl/transforms/` (registre dans `xdsl/transforms/__init__.py`). Les passes situées dans `xdsl/backend/` ne sont pas couvertes ici.

Les passes sont regroupées par thème. Pour chaque pass : `nom-cli` — fichier source — rôle. Lorsque pertinent, un exemple `avant → après` est fourni.

---

## 1. Optimisations génériques

### `canonicalize` — `canonicalize.py`
Applique tous les patterns de canonicalisation enregistrés (folding, simplifications structurelles, élimination d'identités).

```mlir
%c1 = arith.constant 1 : i32
%r  = arith.addi %x, %c0 : i32   // %c0 = 0
// →
%r  = %x
```

### `cse` — `common_subexpression_elimination.py`
Élimination des sous-expressions communes (DCE-aware).

```mlir
%a = arith.addi %x, %y
%b = arith.addi %x, %y   // doublon
// →
%a = arith.addi %x, %y
// %b est remplacé par %a
```

### `dce` — `dead_code_elimination.py`
Supprime les opérations sans effet de bord et sans utilisateurs.

### `licm` — `loop_invariant_code_motion.py`
Sort des boucles toute opération sans effet de bord dont les opérandes sont définis hors de la boucle.

```mlir
scf.for %i = ... {
  %k = arith.addi %a, %b   // invariant
  use(%k, %i)
}
// → %k hoisté avant le scf.for
```

### `control-flow-hoist` — `control_flow_hoist.py`
Sort hors d'une op de contrôle de flot (if, for) toute op « hoistable ».

### `constant-fold-interp` — `constant_fold_interp.py`
Utilise l'interpréteur xDSL pour replier en constante toute op pure dont les entrées sont constantes.

### `test-constant-folding`, `test-specialised-constant-folding` — `test_constant_folding.py`
Versions de test du folding constant (pour la chaîne de tests).

### `reconcile-unrealized-casts` — `reconcile_unrealized_casts.py`
Élimine les `builtin.unrealized_conversion_cast` introduits par des lowerings partiels lorsqu'ils s'annulent.

### `shape-inference` — `shape_inference.py`
Applique tous les patterns d'inférence de forme enregistrés (notamment pour `stencil`).

### `frontend-desymrefy` — `desymref.py`
Transforme les références symboliques (variables de frontend) en SSA pure.

### `mlir-opt` — `mlir_opt.py`
Pass de pont qui appelle l'outil externe `mlir-opt` avec des arguments donnés. Échoue si `mlir-opt` est absent.

### `transform-interpreter` — `transform_interpreter.py`
Interprète une séquence du dialecte `transform`, point d'entrée par défaut `__transform_main`.

### `test-transform-dialect-erase-schedule` — `test_transform_dialect_erase_schedule.py`
Efface les `transform.named_sequence` (utilisé après `transform-interpreter`).

### `verify-register-allocation` — `verify_register_allocation.py`
Vérifie qu'un registre utilisé en entrée/sortie est bien à sa dernière utilisation (sous l'hypothèse de dominance).

### `apply-individual-rewrite` — `individual_rewrite.py`
Applique un unique pattern, identifié par index et nom, à une op désignée. Sert à l'outillage.

---

## 2. PDL et égalité par saturation (eqsat)

### `apply-pdl` — `apply_pdl.py`
Applique des patterns PDL contenus dans le module ou dans `pdl_file`.

### `apply-pdl-interp` — `apply_pdl_interp.py`
Applique des patterns sous forme `pdl_interp` (forme déjà compilée).

### `convert-pdl-to-pdl-interp` — `convert_pdl_to_pdl_interp/conversion.py`
Compile les patterns `pdl` en `pdl_interp` (port partiel de MLIR).

### `apply-eqsat-pdl` — `apply_eqsat_pdl.py`
Applique des patterns PDL via saturation d'équivalence (e-graph).

### `apply-eqsat-pdl-interp` — `apply_eqsat_pdl_interp.py`
Variante saturée du moteur `pdl_interp` (avec `max_iterations`, défaut 20).

### `convert-pdl-interp-to-eqsat-pdl-interp` — `convert_pdl_interp_to_eqsat_pdl_interp.py`
Adapte un programme `pdl_interp` à l'usage saturé.

### `eqsat-create-eclasses` — `eqsat_create_eclasses.py`
Crée les e-classes initiales en enveloppant chaque op dans `eqsat.eclass`.

```mlir
%a = arith.addi %x, %y : i32
// →
%e = eqsat.eclass %a : i32
```

### `eqsat-create-egraphs` — `eqsat_create_egraphs.py`
Insère un `equivalence.graph` autour du corps d'une fonction.

### `eqsat-add-costs` — `eqsat_add_costs.py`
Annote chaque op d'un coût et fait remonter le minimum sur chaque e-classe (point fixe bottom-up).

### `eqsat-extract` — `eqsat_extract.py`
Extrait, à partir des coûts, le sous-programme de coût minimal (`min_cost_index`).

### `eqsat-serialize-egraph` — `eqsat_serialize_egraph.py`
Sérialise l'e-graph courant en JSON sur stdout.

---

## 3. Arithmétique et math

### `arith-add-fastmath` — `arith_add_fastmath.py`
Ajoute des flags fastmath sur les ops flottantes du dialecte `arith` (par défaut `fast`).

```mlir
%a = arith.addf %x, %y : f32
// →
%a = arith.addf %x, %y fastmath<fast> : f32
```

### `expand-math-to-polynomials` — `expand_math_to_polynomials.py`
Approxime des ops `math` via leur série de Taylor (actuellement `math.exp`).

### `approximate-math-with-bitcast` — `approximate_math_with_bitcast.py`
Approxime `math.log`/`math.exp` via des manipulations bitcast — pour environnements basse précision.

### `convert-arith-to-varith` / `convert-varith-to-arith` — `varith_transformations.py`
Convertit des chaînes `arith.add{i,f}` / `arith.mul{i,f}` en une seule op variadique `varith.add` / `varith.mul`, et réciproquement.

```mlir
%t1 = arith.addi %a, %b
%t2 = arith.addi %t1, %c
%t3 = arith.addi %t2, %d
// →
%t  = varith.add %a, %b, %c, %d
```

### `varith-fuse-repeated-operands` — `varith_transformations.py`
Fusionne les occurrences répétées d'un même opérande dans `varith.add`.

```mlir
varith.add %x, %x, %x, %y     // 3 fois %x
// →
%c   = arith.constant 3
%mul = arith.muli %x, %c
varith.add %mul, %y
```

---

## 4. Linalg

### `linalg-generalize-named-ops` — `linalg_generalize_named_ops.py`
Convertit les ops nommées de `linalg` (matmul, add…) en `linalg.generic`.

### `linalg-fuse-multiply-add` — `linalg_transformations.py`
Fusionne `linalg.mul` + `linalg.add` en un `linalg.generic` FMA.

### `lift-arith-to-linalg` — `lift_arith_to_linalg.py`
Promeut des ops `arith` sur tenseurs (`addf`, `subf`, `mulf`) en ops `linalg` correspondantes — utile avant bufferisation.

### `convert-linalg-to-loops` — `convert_linalg_to_loops.py`
Convertit les ops structurées `linalg` en boucles imbriquées parfaites (`scf.for`).

### `convert-linalg-to-memref-stream` — `convert_linalg_to_memref_stream.py`
Convertit `linalg.generic` (sur memref) en `memref_stream.generic`.

### `linalg-to-csl` — `linalg_to_csl.py`
Convertit les ops linalg (mode memref, post-bufferisation) en ops CSL.

### `test-vectorize-matmul` — `test_vectorize_matmul.py`
Pass de test : vectorise `linalg.matmul` selon une stratégie spécifique.

### `test-lower-linalg-to-snitch` — `test_lower_linalg_to_snitch.py`
Pipeline de test pour descendre des microkernels `linalg.generic` vers l'assembleur Snitch.

---

## 5. SCF / boucles

### `convert-scf-to-cf` — `convert_scf_to_cf.py`
Abaisse `scf.for` et `scf.if` en flot de contrôle non structuré (`cf.br`, `cf.cond_br`).

### `convert-scf-to-openmp` — `convert_scf_to_openmp.py`
Convertit `scf.parallel` en `omp.wsloop`. Sans support des réductions.

### `scf-for-loop-flatten` — `scf_for_loop_flatten.py`
Fusionne deux `scf.for` parfaitement imbriqués lorsque l'espace interne tient pile dans le pas externe.

```mlir
scf.for %i = 0 to N step 4 {
  scf.for %j = %i to %i+4 step 1 { use(%j) }
}
// →
scf.for %k = 0 to N step 1 { use(%k) }
```

### `scf-for-loop-range-folding` — `scf_for_loop_range_folding.py`
Replie une multiplication d'IV dans les bornes/pas de la boucle.

### `scf-for-loop-unroll` — `scf_for_loop_unroll.py`
Déroule complètement les `scf.for` à bornes et pas constants.

### `scf-parallel-loop-tiling` — `scf_parallel_loop_tiling.py`
Tuilage des `scf.parallel` selon `parallel_loop_tile_sizes`.

### `lower-affine` — `lower_affine.py`
Abaisse les ops `affine` (`affine.for`, `affine.load`, `affine.apply`…) vers `scf` + `arith` + `memref`.

---

## 6. Stencil

### `stencil-bufferize` — `stencil_bufferize.py`
Bufferise le dialecte stencil : élimine `load`/`store`/`buffer`/`combine` pour produire des stencils sur champs.

### `stencil-inlining` — `stencil_inlining.py`
Inline un `stencil.apply` dans un consommateur `stencil.apply` lorsque c'est profitable.

### `stencil-unroll` — `stencil_unroll.py`
Déroule le corps d'un `stencil.apply` selon `unroll_factor`.

### `stencil-shape-minimize` — `stencil_shape_minimize.py`
Réduit la taille des `stencil.field` sur-alloués.

### `stencil-storage-materialization` — `experimental/stencil_storage_materialization.py`
Insère un `stencil.buffer` quand une sortie d'`apply` n'est pas déjà mappée à un stockage.

### `stencil-tensorize-z-dimension` — `experimental/stencil_tensorize_z_dimension.py`
Tensorise la dimension Z des opérations stencil (puis backpropage les types).

### `convert-stencil-to-ll-mlir` — `experimental/convert_stencil_to_ll_mlir.py`
Abaisse le stencil vers le MLIR « bas » (memref/scf/arith).

### `hls-convert-stencil-to-ll-mlir` — `experimental/hls_convert_stencil_to_ll_mlir.py`
Variante orientée HLS/FPGA.

### `lower-hls` / `replace-incompatible-fpga` — `experimental/lower_hls.py`, `experimental/replace_incompatible_fpga.py`
Étapes de lowering HLS et substitution d'ops non supportées par le backend FPGA.

---

## 7. CSL (Cerebras)

### `convert-stencil-to-csl-stencil` — `convert_stencil_to_csl_stencil.py`
Adapte un stencil générique à `csl_stencil` (paramètre `num_chunks` pour le découpage de communication).

### `csl-stencil-bufferize` — `csl_stencil_bufferize.py`
Bufferise `csl_stencil` ; injecte `apply.recv_chunk_cb.accumulator` dans les `outs` linalg pour faciliter la bufferisation.

### `csl-stencil-handle-async-flow` — `csl_stencil_handle_async_flow.py`
Traduit le flot de contrôle synchrone autour d'un `csl_stencil.apply` asynchrone en graphe d'appels `csl.func` (cond/body/inc/post).

### `csl-stencil-materialize-stores` — `csl_stencil_materialize_stores.py`
Crée les stores à partir des valeurs cédées par `apply.done_exchange.yield`, hors région bord.

### `csl-stencil-set-global-coeffs` — `csl_stencil_set_global_coeffs.py`
Génère un unique appel `coeff` global si tous les `csl_stencil.apply` partagent les mêmes coefficients.

### `csl-stencil-to-csl-wrapper` — `csl_stencil_to_csl_wrapper.py`
Encapsule chaque fonction top-level en `csl_wrapper.module`.

### `csl-wrapper-hoist-buffers` — `csl_wrapper_hoist_buffers.py`
Hoiste les `memref.alloc` au niveau du `csl_wrapper.program_module`.

### `lower-csl-stencil` — `lower_csl_stencil.py`
Abaisse `csl_stencil.{access,apply,yield}` en appels d'API CSL et `csl.func`.

### `lower-csl-wrapper` — `lower_csl_wrapper.py`
Décompose un `csl_wrappermodule` en deux `csl.module` (layout + program).

### `memref-to-dsd` — `memref_to_dsd.py`
Abaisse les ops `memref` vers les DSD CSL.

---

## 8. Memref / Memref-Stream / Tenseur

### `empty-tensor-to-alloc-tensor` — `empty_tensor_to_alloc_tensor.py`
Convertit `tensor.empty` en `bufferization.alloc_tensor`.

### `convert-ml-program-to-memref` — `convert_ml_program_to_memref.py`
Convertit `ml_program` (niveau tenseur) en `memref` (avec ops bufferization de pont).

### `convert-memref-to-ptr` — `convert_memref_to_ptr.py`
Abaisse `memref.load`/`store`/etc. en arithmétique de pointeurs (`ptr`).

### `loop-hoist-memref` — `loop_hoist_memref.py`
Sort des `memref.load`/`store` invariants hors d'une boucle.

### `memref-streamify` — `memref_streamify.py`
Déplace un `memref.generic` (sur memref) dans une région streaming pour le transformer en générique sur streams.

### `memref-stream-legalize` — `memref_stream_legalize.py`
Légalise le payload et les bornes d'un `memref_stream.generic` pour le streaming.

### `memref-stream-fold-fill` — `memref_stream_fold_fill.py`
Replie un `memref_stream.fill` directement dans le `memref_stream.generic` consommateur.

### `memref-stream-generalize-fill` — `memref_stream_generalize_fill.py`
Convertit `memref_stream.fill` en `memref_stream.generic` équivalent.

### `memref-stream-infer-fill` — `memref_stream_infer_fill.py`
Détecte les `memref_stream.generic` représentables comme `memref_stream.fill`.

### `memref-stream-interleave` — `memref_stream_interleave.py`
Tuile la dimension parallèle la plus interne d'un `memref_stream.generic` (paramètre `pipeline-depth`).

### `memref-stream-tile-outer-loops` — `memref_stream_tile_outer_loops.py`
Matérialise des boucles autour d'un `memref_stream.generic` quand ses bornes non-1 dépassent un seuil.

### `memref-stream-unnest-out-parameters` — `memref_stream_unnest_out_parameters.py`
Restreint les affine maps des sorties à ne dépendre que des index « parallel ».

### `convert-memref-stream-to-loops` — `convert_memref_stream_to_loops.py`
Convertit un `memref_stream.generic` en boucles `scf.for`.

### `convert-memref-stream-to-snitch-stream` — `convert_memref_stream_to_snitch_stream.py`
Convertit `memref_stream.{read,write}` vers leurs équivalents `snitch_stream`.

---

## 9. Pointeurs et vecteurs

### `convert-ptr-to-llvm` — `convert_ptr_to_llvm.py`
Abaisse le dialecte `ptr` vers `llvm`.

### `convert-ptr-to-riscv` — `convert_ptr_to_riscv.py`
Abaisse `ptr` vers RISC-V.

### `convert-ptr-type-offsets` — `convert_ptr_type_offsets.py`
Remplace `ptr.type_offset` par sa valeur entière.

### `convert-vector-to-ptr` — `convert_vector_to_ptr.py`
Abaisse les opérations `vector` (load/store) vers `ptr`.

### `vector-split-load-extract` — `vector_split_load_extract.py`
Remplace un `vector.load` suivi uniquement d'`extract` par des loads scalaires.

```mlir
%v = ptr.load %p : vector<4xi32>
%a = vector.extract %v[1] : i32
// →
%off = arith.constant 4 : index
%p1  = ptr.ptradd %p, %off
%a   = ptr.load %p1 : i32
```

---

## 10. RISC-V / Snitch

### `convert-riscv-scf-for-to-frep` — `convert_riscv_scf_for_to_frep.py`
Convertit `riscv_scf.for` en `riscv_snitch.frep_outer` quand les critères de vérification sont remplis (IV non utilisée…).

### `convert-riscv-to-llvm` — `convert_riscv_to_llvm.py`
Émet les instructions RISC-V comme inline asm LLVM (utilise `.insn` pour les ops custom).

### `riscv-allocate-infinite-registers` — `riscv_allocate_infinite_registers.py`
Alloue des registres infinis (registres SSA virtuels).

### `riscv-allocate-registers` — `riscv_allocate_registers.py`
Allocation finale aux registres physiques.

### `riscv-lower-parallel-mov` — `riscv_lower_parallel_mov.py`
Sépare un `ParallelMovOp` en moves indépendants.

### `riscv-scf-for-infer-constant-step` — `riscv_scf_for_infer_constant_step.py`
Détecte un pas constant pour `riscv_scf.for`.

### `riscv-scf-loop-range-folding` — `riscv_scf_loop_range_folding.py`
Variante RISC-V du folding de la plage d'une boucle.

### `lower-riscv-func` — `lower_riscv_func.py`
Abaisse les `riscv_func.func` (ABI, prologue/épilogue éventuel via `insert_exit_syscall`).

### `lower-snitch` / `inline-snrt` — `lower_snitch.py`, `inline_snrt.py`
Abaisse les ops Snitch et inline les ops `snrt` vers leurs définitions (`arith`, `riscv.csr*`, `riscv_snitch`).

### `snitch-allocate-registers` — `snitch_allocate_registers.py`
Alloue les registres pour les opérations Snitch.

---

## 11. x86

### `convert-scf-to-x86-scf` — `convert_scf_to_x86_scf.py`
Convertit `scf` vers `x86_scf` (paramètre `arch`).

### `convert-x86-scf-to-x86` — `convert_x86_scf_to_x86.py`
Abaisse `x86_scf.for` vers du x86 plat (labels, branches).

### `x86-allocate-registers` — `x86_allocate_registers.py`
Allocation registres pour x86.

### `x86-legalize-for-regalloc` — `x86_legalize_for_regalloc.py`
Légalise avant l'alloc registres, en supprimant les copies redondantes en dernière utilisation.

### `x86-infer-broadcast` — `x86_infer_broadcast.py`
Réécrit un load scalaire suivi d'un `vpbroadcastq` en un broadcast-load.

```asm
mov   %tmp,  [%mem]
vpbroadcastq %dst, %tmp
; →
vbroadcastsd %dst, [%mem]
```

---

## 12. GPU / OpenMP

### `memref-to-gpu` — `gpu_allocs.py`
Convertit allocations memref en allocations GPU.

### `gpu-map-parallel-loops` — `gpu_map_parallel_loops.py`
Annote les `scf.parallel` avec un mapping vers la hiérarchie de threads/blocks GPU.

---

## 13. MPI / DMP (stencil distribué)

### `canonicalize-dmp` — `canonicalize_dmp.py`
Canonicalise les `dmp.swap`.

### `distribute-stencil` — `experimental/dmp/stencil_global_to_local.py`
Décompose un stencil global en domaines locaux (stratégie `2d-grid` ou `3d-grid`). Applique l'inférence de forme stencil.

### `dmp-to-mpi` — `experimental/dmp/stencil_global_to_local.py`
Abaisse les ops `dmp` vers le dialecte `mpi` (avec `mpi_init` et `generate_debug_prints` optionnels).

### `lower-mpi` — `lower_mpi.py`
Abaisse `mpi` vers des appels C de la bibliothèque MPI (à partir de `MpiLibraryInfo`).

---

## 14. Print / I/O

### `printf-to-llvm` — `printf_to_llvm.py`
Convertit `printf.print_format` en appels à `printf` LLVM avec création de chaînes globales.

### `printf-to-putchar` — `printf_to_putchar.py`
Convertit `printf.print_int` en boucle d'appels à `putchar`.

---

## 15. JAX / fonctions

### `jax-use-donated-arguments` — `jax_use_donated_arguments.py`
Réutilise les arguments « donated » comme tampons de sortie. Option `remove_matched_outputs`.

### `function-persist-arg-names` — `function_transformations.py`
Persiste les `name_hint` des arguments `func.func` vers `arg_attrs` (clé `llvm.name`).

```mlir
func.func @f(%arg_name: i32) -> ...
// →
func.func @f(%arg_name: i32 {"llvm.name" = "arg_name"}) -> ...
```

### `test-add-timers-to-top-level-funcs` — `function_transformations.py`
Insère `timer_start`/`timer_end` autour des fonctions top-level (pass de bench).

### `function-constant-pinning` — `experimental/function_constant_pinning.py`
Génère une copie spécialisée d'une fonction où une SSA-value est fixée à une constante, et insère le dispatch dynamique.

### `func-to-pdl-rewrite` — `experimental/func_to_pdl_rewrite.py`
Transforme une fonction en `pdl.rewrite`.

---

## Résumé

- **~120 passes** sont enregistrées. Elles forment plusieurs pipelines :
  - Frontend → MLIR haut niveau : `frontend-desymrefy`, `lift-arith-to-linalg`, `linalg-generalize-named-ops`.
  - MLIR haut → bas : chaînes `linalg → memref-stream → loops/scf → cf/llvm` ou `... → riscv/x86/csl/llvm`.
  - Optimisations transverses : `canonicalize`, `cse`, `dce`, `licm`, `control-flow-hoist`, `constant-fold-interp`.
  - Réécriture programmable : `apply-pdl[-interp]`, `apply-eqsat-pdl[-interp]`, `eqsat-*`.
  - Cibles spécialisées : RISC-V/Snitch, x86, CSL, GPU/OpenMP, MPI/DMP, HLS/FPGA.
- Beaucoup de passes sont des reprises directes des passes MLIR de même nom (ex. `scf-for-loop-range-folding`, `lower-affine`, `convert-scf-to-cf`).
