#include "rubiks/cube_state.hpp"
#include <bit>
#include <iostream>

int main() {
    using namespace rubiks;
    constexpr CubeState solved_cube;
    static_assert(solved_cube.twist == 0 && solved_cube.flip == 0);
    static_assert(solved_cube.slice_mask == 240);
    for (int slice = 0; slice < 495; ++slice) {
        const auto mask = static_cast<unsigned>(slice_mapping.masks[slice]);
        if (std::popcount(mask) != 4 || slice_mapping.coordinate[mask] != slice) return 1;
    }
    CubeState cube;
    const int solved_slice = slice_mapping.coordinate[240];
    if (cube.phase1_state_corners() != solved_slice || cube.phase1_state_edges() != solved_slice) return 2;
    for (int i = 0; i < 500; ++i) {
        cube = apply_move(cube, phase1_moves[(i * 7 + i / 18) % 18]);
        int expected_twist = 0, expected_flip = 0, expected_mask = 0;
        for (int j = 0; j < 7; ++j) expected_twist = expected_twist * 3 + cube.co[j];
        for (int j = 0; j < 11; ++j) expected_flip = expected_flip * 2 + cube.eo[j];
        for (int j = 0; j < 12; ++j) if (cube.ep[j] >= 4 && cube.ep[j] <= 7) expected_mask |= 1 << j;
        const int slice = slice_mapping.coordinate[expected_mask];
        const int corners = cube.phase1_state_corners();
        const int edges = cube.phase1_state_edges();
        if (corners != expected_twist * 495 + slice || edges != expected_flip * 495 + slice) return 3;
        if (corners < 0 || corners >= 2187 * 495 || edges < 0 || edges >= 2048 * 495) return 4;
        if (cube.phase1_state_corner() != corners) return 5;
        CubeState copied(cube);
        if (copied.phase1_state_corners() != corners || copied.phase1_state_edges() != edges) return 6;
    }
    // Legal orientations reaching both maximal independent coordinates.
    std::array<int,8> co{2,2,2,2,2,2,2,1};
    std::array<int,12> eo{1,1,1,1,1,1,1,1,1,1,1,1};
    CubeState maximum(solved_corners,co,solved_edges,eo);
    if (maximum.twist != 2186 || maximum.flip != 2047) return 7;
    if (maximum.phase1_state_corners() != 2186 * 495 + solved_slice ||
        maximum.phase1_state_edges() != 2047 * 495 + solved_slice) return 8;
    std::cout << "495 slice mappings, 500 state transitions, and coordinate boundaries verified\n";
}
