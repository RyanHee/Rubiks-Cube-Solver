#pragma once

#include "rubiks/cube_state.hpp"
#include <queue>
#include <vector>

namespace rubiks {

struct Tables {
    std::vector<int> corner_distance;
    std::vector<int> edge_distance;
    std::vector<int> phase2_corner_distance;
    std::vector<int> phase2_edge_distance;
    Tables() : corner_distance(2187 * 495, 255), edge_distance(2048 * 495, 255),
               phase2_corner_distance(40320 * 24, 255),
               phase2_edge_distance(40320 * 24, 255) {}
};

inline Tables generate_tables() {
    std::queue<CubeState> qu;
    Tables ans{};
    qu.push(solved_cube);
    ans.corner_distance[solved_cube.phase1_state_corners()] = 0;
    
    while (!qu.empty()) {
        CubeState u = qu.front();
        qu.pop();
        const int u_state = u.phase1_state_corners();
        for (Move mv : phase1_moves) {
            CubeState v = apply_move(u, mv);
            const int v_state = v.phase1_state_corners();
            if (ans.corner_distance[v_state] == 255) {
                ans.corner_distance[v_state] = ans.corner_distance[u_state] + 1;
                qu.push(v);
            }
        }
    }

    qu.push(solved_cube);
    ans.edge_distance[solved_cube.phase1_state_edges()] = 0;
    
    while (!qu.empty()) {
        CubeState u = qu.front();
        qu.pop();
        const int u_state = u.phase1_state_edges();
        for (Move mv : phase1_moves) {
            CubeState v = apply_move(u, mv);
            const int v_state = v.phase1_state_edges();
            if (ans.edge_distance[v_state] == 255) {
                ans.edge_distance[v_state] = ans.edge_distance[u_state] + 1;
                qu.push(v);
            }
        }
    }

    // Phase 2 ignores orientations, and only uses moves preserving its subgroup.
    qu.push(solved_cube);
    ans.phase2_corner_distance[solved_cube.phase2_state_corners()] = 0;
    while (!qu.empty()) {
        CubeState u = qu.front();
        qu.pop();
        const int u_state = u.phase2_state_corners();
        for (Move mv : phase2_moves) {
            CubeState v = apply_move(u, mv);
            const int v_state = v.phase2_state_corners();
            if (ans.phase2_corner_distance[v_state] == 255) {
                ans.phase2_corner_distance[v_state] = ans.phase2_corner_distance[u_state] + 1;
                qu.push(v);
            }
        }
    }

    qu.push(solved_cube);
    ans.phase2_edge_distance[solved_cube.phase2_state_edges()] = 0;
    while (!qu.empty()) {
        CubeState u = qu.front();
        qu.pop();
        const int u_state = u.phase2_state_edges();
        for (Move mv : phase2_moves) {
            CubeState v = apply_move(u, mv);
            const int v_state = v.phase2_state_edges();
            if (ans.phase2_edge_distance[v_state] == 255) {
                ans.phase2_edge_distance[v_state] = ans.phase2_edge_distance[u_state] + 1;
                qu.push(v);
            }
        }
    }

    return ans;
}

}
