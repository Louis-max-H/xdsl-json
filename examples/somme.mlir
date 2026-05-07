builtin.module {
  func.func private @print_int(i64) -> ()
  func.func @xdsl_main(%max: i64) -> i64 {
    %0 = memref.alloca() : memref<1xi64>
    %1 = arith.constant 0 : index
    memref.store %max, %0[%1] : memref<1xi64>
    %2 = arith.constant 0 : i64
    %3 = memref.alloca() : memref<1xi64>
    %4 = arith.constant 0 : index
    memref.store %2, %3[%4] : memref<1xi64>
    %5 = arith.constant 0 : i64
    %6 = memref.alloca() : memref<1xi64>
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
      %14 = memref.load %0[%13] : memref<1xi64>
      func.call @print_int(%14) : (i64) -> ()
      %15 = arith.constant 0 : index
      %16 = memref.load %3[%15] : memref<1xi64>
      %17 = arith.constant 0 : index
      %18 = memref.load %6[%17] : memref<1xi64>
      %19 = arith.addi %16, %18 : i64
      %20 = arith.constant 0 : index
      memref.store %19, %3[%20] : memref<1xi64>
      %21 = arith.constant 0 : index
      %22 = memref.load %6[%21] : memref<1xi64>
      %23 = arith.constant 1 : i64
      %24 = arith.addi %22, %23 : i64
      %25 = arith.constant 0 : index
      memref.store %24, %6[%25] : memref<1xi64>
      scf.yield
    }
    %26 = arith.constant 0 : index
    %27 = memref.load %3[%26] : memref<1xi64>
    func.call @print_int(%27) : (i64) -> ()
    %28 = arith.constant 0 : index
    %29 = memref.load %3[%28] : memref<1xi64>
    func.return %29 : i64
  }
}
