module {
  llvm.func @malloc(i64) -> !llvm.ptr
  llvm.func @print_int(i64) attributes {sym_visibility = "private"}
  llvm.func @main() -> i64 {
    %0 = llvm.mlir.zero : !llvm.ptr
    %1 = llvm.mlir.constant(42 : i64) : i64
    %2 = llvm.mlir.constant(0 : i64) : i64
    %3 = llvm.mlir.constant(8 : i64) : i64
    %4 = llvm.getelementptr %0[1] : (!llvm.ptr) -> !llvm.ptr, i64
    %5 = llvm.ptrtoint %4 : !llvm.ptr to i64
    %6 = llvm.call @malloc(%5) : (i64) -> !llvm.ptr
    llvm.store %1, %6 : i64, !llvm.ptr
    %7 = llvm.load %6 : !llvm.ptr -> i64
    llvm.call @print_int(%7) : (i64) -> ()
    %8 = llvm.load %6 : !llvm.ptr -> i64
    %9 = llvm.add %8, %3 : i64
    %10 = llvm.getelementptr %0[1] : (!llvm.ptr) -> !llvm.ptr, i64
    %11 = llvm.ptrtoint %10 : !llvm.ptr to i64
    %12 = llvm.call @malloc(%11) : (i64) -> !llvm.ptr
    llvm.store %9, %12 : i64, !llvm.ptr
    %13 = llvm.load %12 : !llvm.ptr -> i64
    llvm.call @print_int(%13) : (i64) -> ()
    llvm.return %2 : i64
  }
}

