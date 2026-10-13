#include "rubiks/cube_state.hpp"
#include <cstdlib>
#include <string>
#include <utility>

int main(int argc, char** argv) {
    using namespace rubiks;
    CubeState cube;
    if (argc == 1) {
        for (int i = 0; i < 200; ++i) {
            cube = apply_move(cube, static_cast<Move>((i * 7) % 18));
            assert_valid_cube(cube);
            (void)phase1_complete(cube);
            (void)phase2_complete(cube);
            (void)solved(cube);
        }
        return 0;
    }
    const std::string invalid = argv[1];
    if (invalid == "cp_low") cube.cp[0] = -1;
    if (invalid == "cp_high") cube.cp[0] = 8;
    if (invalid == "cp_duplicate") cube.cp[0] = 1;
    if (invalid == "ep_low") cube.ep[0] = -1;
    if (invalid == "ep_high") cube.ep[0] = 12;
    if (invalid == "ep_duplicate") cube.ep[0] = 1;
    if (invalid == "co_low") cube.co[0] = -1;
    if (invalid == "co_high") cube.co[0] = 3;
    if (invalid == "eo_low") cube.eo[0] = -1;
    if (invalid == "eo_high") cube.eo[0] = 2;
    if (invalid == "twist_sum") cube.co[0] = 1;
    if (invalid == "flip_sum") cube.eo[0] = 1;
    if (invalid == "parity") std::swap(cube.cp[0], cube.cp[1]);
    if (invalid == "phase1_incomplete") cube = apply_move(cube, Move::R);
    if (invalid == "move_low" || invalid == "move_high") {
        (void)apply_move(cube, static_cast<Move>(invalid == "move_low" ? -1 : 18));
        return 0;
    }
    if (argc != 3) return 2;
    const std::string operation = argv[2];
    if (operation == "apply") (void)apply_move(cube, Move::R);
    else if (operation == "phase1") (void)phase1_complete(cube);
    else if (operation == "phase2") (void)phase2_complete(cube);
    else if (operation == "solved") (void)solved(cube);
    else if (operation == "phase2_corners") (void)cube.phase2_state_corners();
    else if (operation == "phase2_edges") (void)cube.phase2_state_edges();
    else return 2;
}
