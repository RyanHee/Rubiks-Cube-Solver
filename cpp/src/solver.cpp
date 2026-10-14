#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <unordered_set>
#include <vector>
#include "rubiks/cube_state.hpp"
#include "rubiks/solver.hpp"
#include "rubiks/table.hpp"

const rubiks::Tables tables = rubiks::generate_tables();

std::vector<rubiks::Move> phase1(const rubiks::CubeState &root) {
    auto dist = [&](const rubiks::CubeState &cube) {
        return std::max(tables.corner_distance[cube.phase1_state_corners()], tables.edge_distance[cube.phase1_state_edges()]);
    };

    int bound = dist(root);
    int nbound = std::numeric_limits<int>::max();
    std::vector<rubiks::Move> ans;
    std::unordered_set<rubiks::CubeKey, rubiks::CubeKeyHash> vis;
    auto dfs = [&](this auto &&self, const rubiks::CubeState &u, std::vector<rubiks::Move> &moves, int prev_face) -> void {
        if (nbound == -1) {
            return;
        }
        const int f = static_cast<int>(moves.size()) + dist(u);
        if (f > bound) {
            nbound = std::min(nbound, f);
            return;
        }
        if (rubiks::phase1_complete(u)) {
            nbound = -1;
            ans = moves;
            return;
        }
        const rubiks::CubeKey key = rubiks::make_key(u);
        if (!vis.insert(key).second) {
            return;
        }
        for (rubiks::Move mv : rubiks::phase1_moves) {
            int face = static_cast<int>(mv) / 3;
            if (face == prev_face) {
                continue;
            }
            rubiks::CubeState v = rubiks::apply_move(u, mv);
            rubiks::CubeKey ky = rubiks::make_key(v);
            if (!vis.count(ky)) {
                moves.push_back(mv);
                self(v, moves, face);
                moves.pop_back();
                if (nbound == -1) {
                    break;
                }
            }
        }
        vis.erase(key);
    };

    while (bound <= 12) {
        nbound = std::numeric_limits<int>::max();
        vis.clear();
        std::vector<rubiks::Move> moves;
        dfs(root, moves, -1);
        if (nbound == -1) {
            return ans;
        }
        if (nbound == std::numeric_limits<int>::max()) {
            break;
        }
        bound = nbound;
    }

    throw std::runtime_error("No phase-1 solution found within 12 moves");
}


std::vector<rubiks::Move> phase2(const rubiks::CubeState &root) {
    if (!rubiks::phase1_complete(root)) {
        throw std::invalid_argument("Phase 2 requires a phase-1-complete cube");
    }
    auto dist = [&](const rubiks::CubeState &cube) {
        return std::max(tables.phase2_corner_distance[cube.phase2_state_corners()], tables.phase2_edge_distance[cube.phase2_state_edges()]);
    };

    int bound = dist(root);
    int nbound = std::numeric_limits<int>::max();
    std::vector<rubiks::Move> ans;
    std::unordered_set<rubiks::CubeKey, rubiks::CubeKeyHash> vis;
    auto dfs = [&](this auto &&self, const rubiks::CubeState &u, std::vector<rubiks::Move> &moves, int prev_face) -> void {
        if (nbound == -1) {
            return;
        }
        const int f = static_cast<int>(moves.size()) + dist(u);
        if (f > bound) {
            nbound = std::min(nbound, f);
            return;
        }
        if (rubiks::solved(u)) {
            nbound = -1;
            ans = moves;
            return;
        }
        const rubiks::CubeKey key = rubiks::make_key(u);
        if (!vis.insert(key).second) {
            return;
        }
        for (rubiks::Move mv : rubiks::phase2_moves) {
            int face = static_cast<int>(mv) / 3;
            if (face == prev_face) {
                continue;
            }
            rubiks::CubeState v = rubiks::apply_move(u, mv);
            rubiks::CubeKey ky = rubiks::make_key(v);
            if (!vis.count(ky)) {
                moves.push_back(mv);
                self(v, moves, face);
                moves.pop_back();
                if (nbound == -1) {
                    break;
                }
            }
        }
        vis.erase(key);
    };

    while (bound <= 18) {
        nbound = std::numeric_limits<int>::max();
        vis.clear();
        std::vector<rubiks::Move> moves;
        dfs(root, moves, -1);
        if (nbound == -1) {
            return ans;
        }
        if (nbound == std::numeric_limits<int>::max()) {
            break;
        }
        bound = nbound;
    }

    throw std::runtime_error("No phase-2 solution found within 18 moves");
}



#ifndef RUBIKS_SOLVER_NO_MAIN
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

    if (!fin) {
        std::cerr << "Cube file must contain 8 cp, 8 co, 12 ep, and 12 eo integers\n";
        return 1;
    }

    rubiks::CubeState root(cp, co, ep, eo);

    std::vector<rubiks::Move> moves;
    std::vector<rubiks::Move> phase1_moves = phase1(root);
    moves.insert(moves.end(), phase1_moves.begin(), phase1_moves.end());

    rubiks::CubeState root2(root);
    for (rubiks::Move mv : phase1_moves) {
        root2 = rubiks::apply_move(root2, mv);
    }

    const auto phase2_moves = phase2(root2);
    moves.insert(moves.end(), phase2_moves.begin(), phase2_moves.end());

    constexpr std::array<const char*, 18> move_names{
        "U", "U2", "U'", "R", "R2", "R'", "F", "F2", "F'",
        "D", "D2", "D'", "L", "L2", "L'", "B", "B2", "B'"
    };
    for (std::size_t i = 0; i < moves.size(); ++i) {
        if (i != 0) std::cout << ' ';
        std::cout << move_names[static_cast<std::size_t>(moves[i])];
    }
    std::cout << '\n';
}
#endif
