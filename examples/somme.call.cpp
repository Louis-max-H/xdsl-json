#include <cstdint>
#include <cstdio>
#include <iostream>

extern "C" {
    int64_t xdsl_main(int64_t arg0);

    void print_int(int64_t value) {
        std::printf("%ld\n", static_cast<long>(value));
    }
}

int main() {
    const int64_t result = xdsl_main(10);
    std::cout << "xdsl_main(10) = " << result << '\n';
    return 0;
}
