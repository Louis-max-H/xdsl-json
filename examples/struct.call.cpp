#include <cstdint>
#include <cstdio>
#include <iostream>

extern "C" {
    struct noeud {
        int capacite;
        int temperature;
    };

    int64_t xdsl_main(noeud arg0);

    void print_int(int64_t value) {
        std::printf("%ld\n", static_cast<long>(value));
    }
}

int main() {
    noeud n {1, 2};
    const int64_t result = xdsl_main(n);
    std::cout << "Value of capacite : xdsl_main(n) = " << result << '\n';
    return 0;
}
