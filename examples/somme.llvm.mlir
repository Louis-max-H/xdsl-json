module {
  llvm.func @malloc(i64) -> !llvm.ptr
  llvm.func @main(%arg0: i64) -> i64 {
    %0 = llvm.mlir.zero : !llvm.ptr
    %1 = llvm.mlir.constant(1 : i64) : i64
    %2 = llvm.mlir.constant(0 : i64) : i64
    %3 = llvm.getelementptr %0[1] : (!llvm.ptr) -> !llvm.ptr, i64
    %4 = llvm.ptrtoint %3 : !llvm.ptr to i64
    %5 = llvm.call @malloc(%4) : (i64) -> !llvm.ptr
    llvm.store %arg0, %5 : i64, !llvm.ptr
    %6 = llvm.getelementptr %0[1] : (!llvm.ptr) -> !llvm.ptr, i64
    %7 = llvm.ptrtoint %6 : !llvm.ptr to i64
    %8 = llvm.call @malloc(%7) : (i64) -> !llvm.ptr
    llvm.store %2, %8 : i64, !llvm.ptr
    %9 = llvm.getelementptr %0[1] : (!llvm.ptr) -> !llvm.ptr, i64
    %10 = llvm.ptrtoint %9 : !llvm.ptr to i64
    %11 = llvm.call @malloc(%10) : (i64) -> !llvm.ptr
    llvm.store %2, %11 : i64, !llvm.ptr
    llvm.br ^bb1
  ^bb1:  // 2 preds: ^bb0, ^bb2
    %12 = llvm.load %11 : !llvm.ptr -> i64
    %13 = llvm.load %5 : !llvm.ptr -> i64
    %14 = llvm.icmp "slt" %12, %13 : i64
    llvm.cond_br %14, ^bb2, ^bb3
  ^bb2:  // pred: ^bb1
    %15 = llvm.load %8 : !llvm.ptr -> i64
    %16 = llvm.load %11 : !llvm.ptr -> i64
    %17 = llvm.add %15, %16 : i64
    llvm.store %17, %8 : i64, !llvm.ptr
    %18 = llvm.load %11 : !llvm.ptr -> i64
    %19 = llvm.add %18, %1 : i64
    llvm.store %19, %11 : i64, !llvm.ptr
    llvm.br ^bb1
  ^bb3:  // pred: ^bb1
    %20 = llvm.load %8 : !llvm.ptr -> i64
    llvm.return %20 : i64
  }
}

