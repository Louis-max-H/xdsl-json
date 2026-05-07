builtin.module {
  func.func private @print_int(i64) -> ()
  func.func @main() -> i64 {
    %0 = arith.constant 42 : i64
    %1 = memref.alloc() : memref<1xi64>
    %2 = arith.constant 0 : index
    memref.store %0, %1[%2] : memref<1xi64>
    %3 = arith.constant 0 : index
    %4 = memref.load %1[%3] : memref<1xi64>
    func.call @print_int(%4) : (i64) -> ()
    %5 = arith.constant 0 : index
    %6 = memref.load %1[%5] : memref<1xi64>
    %7 = arith.constant 8 : i64
    %8 = arith.addi %6, %7 : i64
    %9 = memref.alloc() : memref<1xi64>
    %10 = arith.constant 0 : index
    memref.store %8, %9[%10] : memref<1xi64>
    %11 = arith.constant 0 : index
    %12 = memref.load %9[%11] : memref<1xi64>
    func.call @print_int(%12) : (i64) -> ()
    %13 = arith.constant 0 : i64
    func.return %13 : i64
  }
}
