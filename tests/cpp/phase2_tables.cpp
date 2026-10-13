#include "rubiks/table.hpp"
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <stdexcept>

void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

int main() {
    using namespace rubiks;

    // Compare Lehmer ranks with independent lexicographic enumeration.
    std::array<int, 8> permutation{0,1,2,3,4,5,6,7};
    int expected_rank = 0;
    do {
        require(detail::permutation_rank(permutation) == expected_rank++, "8-piece rank mismatch");
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    require(expected_rank == 40320, "Missing 8-piece permutations");
    std::array<int, 4> slice{0,1,2,3};
    expected_rank = 0;
    do {
        require(detail::permutation_rank(slice) == expected_rank++, "4-piece rank mismatch");
    } while (std::next_permutation(slice.begin(), slice.end()));
    require(expected_rank == 24, "Missing slice permutations");

    const auto tables = generate_tables();
    for (const auto* distance : {&tables.corner_distance, &tables.edge_distance,
                                 &tables.phase2_corner_distance, &tables.phase2_edge_distance}) {
        require(std::count(distance->begin(), distance->end(), 255) == 0, "Unvisited table entries");
        require(std::count(distance->begin(), distance->end(), 0) == 1, "Goal is not unique");
    }
    require(tables.corner_distance[solved_cube.phase1_state_corners()] == 0, "Phase-1 corner goal changed");
    require(tables.edge_distance[solved_cube.phase1_state_edges()] == 0, "Phase-1 edge goal changed");

    for (bool corners : {true, false}) {
        const auto& distance = corners ? tables.phase2_corner_distance : tables.phase2_edge_distance;
        auto coordinate = [corners](const CubeState& cube) {
            return corners ? cube.phase2_state_corners() : cube.phase2_state_edges();
        };
        require(distance.size() == 40320 * 24, "Wrong phase-2 table size");
        require(coordinate(solved_cube) == 0 && distance[0] == 0, "Wrong phase-2 goal");

        // Full cubie-state paths, without projection pruning, give independent
        // reference distances for all states within two moves of the goal.
        std::map<int, int> shallow{{0, 0}};
        for (Move move : phase2_moves) {
            shallow.try_emplace(coordinate(apply_move(solved_cube, move)), 1);
        }
        for (Move first : phase2_moves) for (Move second : phase2_moves) {
            shallow.try_emplace(coordinate(apply_move(apply_move(solved_cube, first), second)), 2);
        }
        for (const auto& [index, depth] : shallow) {
            require(distance[index] == depth, "Incorrect shallow BFS distance");
        }

        // Hidden permutations must not affect a projected state's transitions.
        CubeState hidden;
        if (corners) { hidden.ep[0] = 1; hidden.ep[1] = 2; hidden.ep[2] = 0; }
        else { hidden.cp[0] = 1; hidden.cp[1] = 2; hidden.cp[2] = 0; }
        require(coordinate(hidden) == 0, "Ignored pieces changed projection");
        for (Move move : phase2_moves) {
            require(coordinate(apply_move(hidden, move)) == coordinate(apply_move(solved_cube, move)),
                    "Projected transition depends on ignored pieces");
        }

        CubeState cube;
        unsigned seed = 2026;
        for (int sample = 0; sample < 2000; ++sample) {
            seed = seed * 1664525u + 1013904223u;
            cube = apply_move(cube, phase2_moves[seed % 10]);
            require(phase1_complete(cube), "Phase-2 move left its subgroup");
            const int index = coordinate(cube);
            require(index >= 0 && index < 40320 * 24, "Coordinate out of range");
            const int depth = distance[index];
            bool descending = depth == 0;
            for (Move move : phase2_moves) {
                const int child_depth = distance[coordinate(apply_move(cube, move))];
                require(std::abs(depth - child_depth) <= 1, "Neighbor-distance inconsistency");
                descending |= child_depth == depth - 1;
            }
            require(descending, "No descending shortest-path neighbor");
        }
        std::cout << (corners ? "Corner" : "Edge") << " phase-2 table: " << distance.size()
                  << " entries, maximum distance " << *std::max_element(distance.begin(), distance.end()) << '\n';
    }
}
