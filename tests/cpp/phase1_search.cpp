#include "rubiks/solver.hpp"
#include "rubiks/table.hpp"
#include <algorithm>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <vector>

void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

rubiks::CubeState scrambled(const std::vector<rubiks::Move>& moves) {
    rubiks::CubeState cube;
    for (auto move : moves) cube = rubiks::apply_move(cube, move);
    return cube;
}

// Independent bounded BFS: no heuristic, state-key cache, or IDA* bound logic.
int shallow_distance(const rubiks::CubeState& root, int maximum) {
    struct Node { rubiks::CubeState cube; int depth; int previous_face; };
    std::queue<Node> queue;
    queue.push({root, 0, -1});
    while (!queue.empty()) {
        const Node node = queue.front();
        queue.pop();
        if (rubiks::phase1_complete(node.cube)) return node.depth;
        if (node.depth == maximum) continue;
        for (auto move : rubiks::phase1_moves) {
            const int face = static_cast<int>(move) / 3;
            if (face != node.previous_face) {
                queue.push({rubiks::apply_move(node.cube, move), node.depth + 1, face});
            }
        }
    }
    return -1;
}

std::vector<rubiks::Move> verify(const rubiks::CubeState& root) {
    const auto saved = root;
    const auto solution = phase1(root);
    require(root == saved, "Search mutated its input");
    require(solution.size() <= 12, "Phase-1 solution exceeds 12 moves");
    auto result = root;
    int previous_face = -1;
    for (auto move : solution) {
        const int face = static_cast<int>(move) / 3;
        require(face != previous_face, "Consecutive moves on the same face");
        previous_face = face;
        result = rubiks::apply_move(result, move);
    }
    require(rubiks::phase1_complete(result), "Returned path does not reach the subgroup");
    return solution;
}

int main() {
    using namespace rubiks;
    require(verify(CubeState()).empty(), "Solved cube needs no moves");
    for (auto move : phase1_moves) {
        auto cube = apply_move(solved_cube, move);
        require(verify(cube).size() == static_cast<std::size_t>(phase1_complete(cube) ? 0 : 1),
                "Incorrect single-move solution length");
    }
    for (const auto& sequence : std::vector<std::vector<Move>>{
        {Move::R, Move::F}, {Move::R, Move::U, Move::F},
        {Move::F, Move::RPrime, Move::B2}, {Move::L, Move::BPrime, Move::U2},
    }) {
        const auto cube = scrambled(sequence);
        const int exact = shallow_distance(cube, 3);
        require(exact >= 0 && verify(cube).size() == static_cast<std::size_t>(exact),
                "IDA* disagrees with independent shallow BFS");
    }

    // Initial h=3, but the shortest subgroup path has length 5. This needs
    // three search iterations and regresses the stale-next-bound infinite loop.
    const auto root = scrambled({Move::L, Move::F2, Move::U2, Move::RPrime,
                                  Move::L, Move::D2, Move::L, Move::L});
    const auto reference_tables = generate_tables();
    const int initial_bound = std::max(
        reference_tables.corner_distance[root.phase1_state_corners()],
        reference_tables.edge_distance[root.phase1_state_edges()]);
    require(initial_bound == 3, "Bound-regression setup changed");
    require(shallow_distance(root, 4) == -1, "Unexpected solution below depth 5");
    require(verify(root).size() == 5, "Multi-iteration search failed");
    // Search again to check that path-state tracking does not leak between calls.
    require(verify(root).size() == 5, "Repeated search differs");
    std::cout << "Phase-1 search: solved, 18 moves, shallow BFS, and multi-bound cases passed\n";
}
