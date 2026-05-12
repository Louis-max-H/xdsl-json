; ModuleID = 'cpp_struct.cpp'
source_filename = "cpp_struct.cpp"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%struct.demo1 = type { i64, i64, i64 }

; Function Attrs: mustprogress noinline norecurse nounwind optnone uwtable
define dso_local noundef i32 @main() #0 {
entry:
  %retval = alloca i32, align 4
  %d1 = alloca %struct.demo1, align 8
  store i32 0, ptr %retval, align 4
  %A = getelementptr inbounds nuw %struct.demo1, ptr %d1, i32 0, i32 0
  store i64 0, ptr %A, align 8
  %A1 = getelementptr inbounds nuw %struct.demo1, ptr %d1, i32 0, i32 0
  store i64 1, ptr %A1, align 8
  %B = getelementptr inbounds nuw %struct.demo1, ptr %d1, i32 0, i32 1
  store i64 2, ptr %B, align 8
  %B2 = getelementptr inbounds nuw %struct.demo1, ptr %d1, i32 0, i32 1
  store i64 3, ptr %B2, align 8
  %C = getelementptr inbounds nuw %struct.demo1, ptr %d1, i32 0, i32 2
  store i64 4, ptr %C, align 8
  %C3 = getelementptr inbounds nuw %struct.demo1, ptr %d1, i32 0, i32 2
  store i64 5, ptr %C3, align 8
  ret i32 0
}

attributes #0 = { mustprogress noinline norecurse nounwind optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 8, !"PIC Level", i32 2}
!1 = !{i32 7, !"PIE Level", i32 2}
!2 = !{i32 7, !"uwtable", i32 2}
!3 = !{i32 7, !"frame-pointer", i32 2}
!4 = !{!"clang version 23.0.0git (https://github.com/llvm/llvm-project.git 0162dbc91d5786dd4195555695759f7620f67f58)"}
