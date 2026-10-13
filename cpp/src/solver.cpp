#include <array>
#include <fstream>
#include <iostream>
#include "rubiks/cube_state.hpp"

rubiks::CubeState phase1(const rubiks::CubeState &root) {
    
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "need cube file\n";
        return 1;
    }

    std::ifstream fin(argv[1]);

    if (!fin) {
        std::cerr << "Could not open: " << argv[1] << '\n';
        return 1;
    }

    std::array<int, 8> cp{};
    std::array<int, 8> co{};
    std::array<int, 12> ep{};
    std::array<int, 12> eo{};

    for (int i = 0; i < 8; i++) {
        fin >> cp[i];
    }
    for (int i = 0; i < 8; i++) {
        fin >> co[i];
    }
    for (int i = 0; i < 12; i++) {
        fin >> ep[i];
    }
    for (int i = 0; i < 12; i++) {
        fin >> eo[i];
    }

    rubiks::CubeState root(cp, co, ep, eo);
    
    
}