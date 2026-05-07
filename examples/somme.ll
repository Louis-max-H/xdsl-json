; ModuleID = 'LLVMDialectModule'
source_filename = "LLVMDialectModule"

declare void @print_int(i64)

define i64 @xdsl_main(i64 %0) {
  br label %2

2:                                                ; preds = %6, %1
  %3 = phi i64 [ %9, %6 ], [ 0, %1 ]
  %4 = phi i64 [ %10, %6 ], [ 0, %1 ]
  %5 = icmp slt i64 %4, %0
  br i1 %5, label %6, label %11

6:                                                ; preds = %2
  %7 = phi i64 [ %3, %2 ]
  %8 = phi i64 [ %4, %2 ]
  call void @print_int(i64 %0)
  %9 = add i64 %7, %8
  %10 = add i64 %8, 1
  br label %2

11:                                               ; preds = %2
  call void @print_int(i64 %3)
  ret i64 %3
}

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
