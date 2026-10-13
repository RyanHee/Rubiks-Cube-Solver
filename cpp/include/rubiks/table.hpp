#pragma once

#include "rubiks/cube_state.hpp"
#include <queue>
#include <vector>

namespace rubiks {

struct Tables {
    std::vector<int> corner_distance;
    std::vector<int> edge_distance;
    Tables() : corner_distance(2187 * 495, 255), edge_distance(2048 * 495, 255) {}
};

inline Tables generate_tables() {
    std::queue<CubeState> qu;
    Tables ans{};
    qu.push(solved_cube);
    ans.corner_distance[solved_cube.phase1_state_corners()] = 0;
    
    while (!qu.empty()) {
        CubeState u = qu.front();
        qu.pop();

        for (Move mv : phase1_moves) {
            CubeState v = apply_move(u, mv);
            if (ans.corner_distance[v.phase1_state_corners()] == 255) {
                ans.corner_distance[v.phase1_state_corners()] = ans.corner_distance[u.phase1_state_corners()] + 1;
                qu.push(v);
            }
        }
    }

    qu.push(solved_cube);
    ans.edge_distance[solved_cube.phase1_state_edges()] = 0;
    
    while (!qu.empty()) {
        CubeState u = qu.front();
        qu.pop();

        for (Move mv : phase1_moves) {
            CubeState v = apply_move(u, mv);
            if (ans.edge_distance[v.phase1_state_edges()] == 255) {
                ans.edge_distance[v.phase1_state_edges()] = ans.edge_distance[u.phase1_state_edges()] + 1;
                qu.push(v);
            }
        }
    }

    return ans;
}

}