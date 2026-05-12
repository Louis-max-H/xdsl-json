#include<stdio.h>

// clang -S -emit-llvm cpp_struct.cpp  

struct demo1 {
    long long A;
    long long B;
    long long C;

};

int main(){
    struct demo1 d1;
    d1.A = 0;
    d1.A = 1;
    d1.B = 2;
    d1.B = 3;
    d1.C = 4;
    d1.C = 5;
    return 0;
}