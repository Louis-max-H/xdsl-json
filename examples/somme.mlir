builtin.module {
  func.func @main(%max: i64) -> i64 {
    %0 = memref.alloc() : memref<1xi64>
    %1 = arith.constant 0 : index
    memref.store %max, %0[%1] : memref<1xi64>
    %2 = arith.constant 0 : i64
    %3 = memref.alloc() : memref<1xi64>
    %4 = arith.constant 0 : index
    memref.store %2, %3[%4] : memref<1xi64>
    %5 = arith.constant 0 : i64
    %6 = memref.alloc() : memref<1xi64>
    %7 = arith.constant 0 : index
    memref.store %5, %6[%7] : memref<1xi64>
    scf.while () : () -> () {
      %8 = arith.constant 0 : index
      %9 = memref.load %6[%8] : memref<1xi64>
      %10 = arith.constant 0 : index
      %11 = memref.load %0[%10] : memref<1xi64>
      %12 = arith.cmpi slt, %9, %11 : i64
      scf.condition(%12)
    } do {
      %13 = arith.constant 0 : index
      %14 = memref.load %3[%13] : memref<1xi64>
      %15 = arith.constant 0 : index
      %16 = memref.load %6[%15] : memref<1xi64>
      %17 = arith.addi %14, %16 : i64
      %18 = arith.constant 0 : index
      memref.store %17, %3[%18] : memref<1xi64>
      %19 = arith.constant 0 : index
      %20 = memref.load %6[%19] : memref<1xi64>
      %21 = arith.constant 1 : i64
      %22 = arith.addi %20, %21 : i64
      %23 = arith.constant 0 : index
      memref.store %22, %6[%23] : memref<1xi64>
      scf.yield
    }
    %24 = arith.constant 0 : index
    %25 = memref.load %3[%24] : memref<1xi64>
    func.return %25 : i64
  }
}
