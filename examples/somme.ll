; ModuleID = 'LLVMDialectModule'
source_filename = "LLVMDialectModule"

declare ptr @malloc(i64)

define i64 @main(i64 %0) {
  %2 = call ptr @malloc(i64 8)
  store i64 %0, ptr %2, align 4
  %3 = call ptr @malloc(i64 8)
  store i64 0, ptr %3, align 4
  %4 = call ptr @malloc(i64 8)
  store i64 0, ptr %4, align 4
  br label %5

5:                                                ; preds = %9, %1
  %6 = load i64, ptr %4, align 4
  %7 = load i64, ptr %2, align 4
  %8 = icmp slt i64 %6, %7
  br i1 %8, label %9, label %15

9:                                                ; preds = %5
  %10 = load i64, ptr %3, align 4
  %11 = load i64, ptr %4, align 4
  %12 = add i64 %10, %11
  store i64 %12, ptr %3, align 4
  %13 = load i64, ptr %4, align 4
  %14 = add i64 %13, 1
  store i64 %14, ptr %4, align 4
  br label %5

15:                                               ; preds = %5
  %16 = load i64, ptr %3, align 4
  ret i64 %16
}

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
