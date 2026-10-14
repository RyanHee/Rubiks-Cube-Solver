#pragma once

#include "rubiks/cube_state.hpp"
#include <vector>

// Return a path into the phase-2 subgroup, without changing root.
// An already phase-1-complete cube returns an empty path.
// Throws std::runtime_error if no path is found within 12 moves.
std::vector<rubiks::Move> phase1(const rubiks::CubeState &root);

// Solve a cube already in the phase-2 subgroup, without changing root.
// Uses only phase2_moves. An already solved cube returns an empty path.
// Throws std::invalid_argument if phase 1 is incomplete, or std::runtime_error
// if no solution is found within 18 moves.
std::vector<rubiks::Move> phase2(const rubiks::CubeState &root);
