; ModuleID = 'LLVMDialectModule'
source_filename = "LLVMDialectModule"

declare ptr @malloc(i64)

declare void @print_int(i64)

define i64 @main() {
  %1 = call ptr @malloc(i64 8)
  store i64 42, ptr %1, align 4
  %2 = load i64, ptr %1, align 4
  call void @print_int(i64 %2)
  %3 = load i64, ptr %1, align 4
  %4 = add i64 %3, 8
  %5 = call ptr @malloc(i64 8)
  store i64 %4, ptr %5, align 4
  %6 = load i64, ptr %5, align 4
  call void @print_int(i64 %6)
  ret i64 0
}

!llvm.module.flags = !{!0}

!0 = !{i32 2, !"Debug Info Version", i32 3}
