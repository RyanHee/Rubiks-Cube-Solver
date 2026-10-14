#include "rubiks/solver.hpp"
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

int shallow_distance(const rubiks::CubeState& root, int maximum) {
    struct Node { rubiks::CubeState cube; int depth; int previous_face; };
    std::queue<Node> queue;
    queue.push({root, 0, -1});
    while (!queue.empty()) {
        const auto node = queue.front(); queue.pop();
        if (rubiks::solved(node.cube)) return node.depth;
        if (node.depth == maximum) continue;
        for (auto move : rubiks::phase2_moves) {
            int face = static_cast<int>(move) / 3;
            if (face != node.previous_face)
                queue.push({rubiks::apply_move(node.cube, move), node.depth + 1, face});
        }
    }
    return -1;
}

std::vector<rubiks::Move> verify(const rubiks::CubeState& root) {
    using namespace rubiks;
    const auto saved = root;
    const auto solution = phase2(root);
    require(root == saved, "Phase 2 mutated its input");
    require(solution.size() <= 18, "Phase 2 exceeded 18 moves");
    auto result = root;
    int previous_face = -1;
    for (auto move : solution) {
        require(std::find(phase2_moves.begin(), phase2_moves.end(), move) != phase2_moves.end(),
                "Returned a forbidden phase-2 move");
        const int face = static_cast<int>(move) / 3;
        require(face != previous_face, "Consecutive same-face moves");
        previous_face = face;
        result = apply_move(result, move);
        require(phase1_complete(result), "Search left the subgroup");
    }
    require(solved(result), "Phase-2 path does not solve the cube");
    return solution;
}

int main() {
    using namespace rubiks;
    require(verify(CubeState()).empty(), "Solved cube needs no moves");
    for (auto move : phase2_moves)
        require(verify(apply_move(solved_cube, move)).size() == 1, "Incorrect single-move solve");
    for (const auto& sequence : std::vector<std::vector<Move>>{
        {Move::R2, Move::U}, {Move::F2, Move::DPrime, Move::L2},
        {Move::U2, Move::B2, Move::D}, {Move::R2, Move::F2, Move::UPrime},
    }) {
        const auto cube = scrambled(sequence);
        const int exact = shallow_distance(cube, 3);
        require(exact >= 0 && verify(cube).size() == static_cast<std::size_t>(exact),
                "Phase 2 disagrees with independent BFS");
    }
    const auto subgroup = scrambled({Move::U, Move::R2, Move::F2, Move::D,
                                    Move::L2, Move::B2, Move::UPrime, Move::R2});
    verify(subgroup);
    verify(subgroup); // Repeat to expose leaked cycle-detection state.

    for (auto move : {Move::R, Move::F, Move::LPrime, Move::BPrime}) {
        bool rejected = false;
        try { (void)phase2(apply_move(solved_cube, move)); }
        catch (const std::invalid_argument&) { rejected = true; }
        require(rejected, "Phase 2 accepted a cube outside its subgroup");
    }

    const auto original = scrambled({Move::U, Move::R2, Move::F2, Move::D, Move::L2, Move::R});
    auto endpoint = original;
    const auto first = phase1(original);
    for (auto move : first) endpoint = apply_move(endpoint, move);
    require(phase1_complete(endpoint), "Phase 1 failed before integration");
    const auto second = verify(endpoint);
    require(!second.empty(), "Integration case must exercise phase-2 moves");
    auto result = original;
    for (auto move : first) result = apply_move(result, move);
    for (auto move : second) result = apply_move(result, move);
    require(solved(result), "Combined phase-1 and phase-2 path failed");
    std::cout << "Phase-2 search and two-phase integration passed\n";
}
