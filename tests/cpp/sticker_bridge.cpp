#include <iostream>
#include "rubiks/cube_state.hpp"

int main() {
    rubiks::CubeState state;
    int move;
    while (std::cin >> move) {
        state = rubiks::apply_move(state, static_cast<rubiks::Move>(move));
        for (int value : state.cp) std::cout << value << ' ';
        for (int value : state.co) std::cout << value << ' ';
        for (int value : state.ep) std::cout << value << ' ';
        for (int value : state.eo) std::cout << value << ' ';
        std::cout << '\n';
    }
}
