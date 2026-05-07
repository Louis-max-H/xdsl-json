builtin.module {
  func.func @main(%a: i64, %b: i64) -> i64 {
    %0 = memref.alloc() : memref<1xi64>
    %1 = arith.constant 0 : index
    memref.store %a, %0[%1] : memref<1xi64>
    %2 = memref.alloc() : memref<1xi64>
    %3 = arith.constant 0 : index
    memref.store %b, %2[%3] : memref<1xi64>
    %4 = arith.constant 0 : index
    %5 = memref.load %0[%4] : memref<1xi64>
    %6 = arith.constant 0 : index
    %7 = memref.load %2[%6] : memref<1xi64>
    %8 = arith.cmpi sgt, %5, %7 : i64
    %9 = scf.if %8 -> (i64) {
      %10 = arith.constant 0 : index
      %11 = memref.load %0[%10] : memref<1xi64>
      scf.yield %11 : i64
    } else {
      %12 = arith.constant 0 : index
      %13 = memref.load %2[%12] : memref<1xi64>
      scf.yield %13 : i64
    }
    func.return %9 : i64
  }
}
