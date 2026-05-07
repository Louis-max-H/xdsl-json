module {
  llvm.func @print_int(i64) attributes {sym_visibility = "private"}
  llvm.func @xdsl_main(%arg0: i64) -> i64 {
    %0 = llvm.mlir.constant(1 : i64) : i64
    %1 = llvm.mlir.constant(0 : i64) : i64
    llvm.br ^bb1(%1, %1 : i64, i64)
  ^bb1(%2: i64, %3: i64):  // 2 preds: ^bb0, ^bb2
    %4 = llvm.icmp "slt" %3, %arg0 : i64
    llvm.cond_br %4, ^bb2(%2, %3 : i64, i64), ^bb3
  ^bb2(%5: i64, %6: i64):  // pred: ^bb1
    %7 = llvm.add %5, %6 : i64
    %8 = llvm.add %6, %0 : i64
    llvm.call @print_int(%7) : (i64) -> ()
    llvm.br ^bb1(%7, %8 : i64, i64)
  ^bb3:  // pred: ^bb1
    llvm.return %2 : i64
  }
}
