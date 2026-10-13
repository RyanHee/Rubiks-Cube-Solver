#pragma once

#include <array>
#include <cstddef>

namespace rubiks {

enum class Move : int {
    U, U2, UPrime,
    R, R2, RPrime,
    F, F2, FPrime,
    D, D2, DPrime,
    L, L2, LPrime,
    B, B2, BPrime
};

constexpr std::array<int, 8> oriented_corners{0, 0, 0, 0, 0, 0, 0, 0};
constexpr std::array<int, 8> solved_corners{0, 1, 2, 3, 4, 5, 6, 7};
constexpr std::array<int, 12> oriented_edges{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
constexpr std::array<int, 12> solved_edges{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};

// source[move][i] = j -> j cubie moving to i
constexpr std::array<std::array<int, 8>, 18> source_c{{
    {3, 0, 1, 2, 4, 5, 6, 7}, // U
    {2, 3, 0, 1, 4, 5, 6, 7}, // U2
    {1, 2, 3, 0, 4, 5, 6, 7}, // UPrime
    {0, 2, 5, 3, 4, 6, 1, 7}, // R
    {0, 5, 6, 3, 4, 1, 2, 7}, // R2
    {0, 6, 1, 3, 4, 2, 5, 7}, // RPrime
    {0, 1, 3, 4, 5, 2, 6, 7}, // F
    {0, 1, 4, 5, 2, 3, 6, 7}, // F2
    {0, 1, 5, 2, 3, 4, 6, 7}, // FPrime
    {0, 1, 2, 3, 7, 4, 5, 6}, // D
    {0, 1, 2, 3, 6, 7, 4, 5}, // D2
    {0, 1, 2, 3, 5, 6, 7, 4}, // DPrime
    {7, 1, 2, 0, 3, 5, 6, 4}, // L
    {4, 1, 2, 7, 0, 5, 6, 3}, // L2
    {3, 1, 2, 4, 7, 5, 6, 0}, // LPrime
    {1, 6, 2, 3, 4, 5, 7, 0}, // B
    {6, 7, 2, 3, 4, 5, 0, 1}, // B2
    {7, 0, 2, 3, 4, 5, 1, 6}  // BPrime
}};

constexpr std::array<std::array<int, 12>, 18> source_e{{
    {3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11}, // U
    {2, 3, 0, 1, 4, 5, 6, 7, 8, 9, 10, 11}, // U2
    {1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11}, // UPrime
    {0, 5, 2, 3, 4, 9, 1, 7, 8, 6, 10, 11}, // R
    {0, 9, 2, 3, 4, 6, 5, 7, 8, 1, 10, 11}, // R2
    {0, 6, 2, 3, 4, 1, 9, 7, 8, 5, 10, 11}, // RPrime
    {0, 1, 4, 3, 8, 2, 6, 7, 5, 9, 10, 11}, // F
    {0, 1, 8, 3, 5, 4, 6, 7, 2, 9, 10, 11}, // F2
    {0, 1, 5, 3, 2, 8, 6, 7, 4, 9, 10, 11}, // FPrime
    {0, 1, 2, 3, 4, 5, 6, 7, 11, 8, 9, 10}, // D
    {0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 8, 9}, // D2
    {0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8}, // DPrime
    {0, 1, 2, 7, 3, 5, 6, 11, 8, 9, 10, 4}, // L
    {0, 1, 2, 11, 7, 5, 6, 4, 8, 9, 10, 3}, // L2
    {0, 1, 2, 4, 11, 5, 6, 3, 8, 9, 10, 7}, // LPrime
    {6, 1, 2, 3, 4, 5, 10, 0, 8, 9, 7, 11}, // B
    {10, 1, 2, 3, 4, 5, 7, 6, 8, 9, 0, 11}, // B2
    {7, 1, 2, 3, 4, 5, 0, 10, 8, 9, 6, 11}, // BPrime
}};

// twist[move][i] = j -> when a cubie is moved to i, it must twist j times
constexpr std::array<std::array<int, 8>, 18> twist_c{{
    {0, 0, 0, 0, 0, 0, 0, 0}, // U
    {0, 0, 0, 0, 0, 0, 0, 0}, // U2
    {0, 0, 0, 0, 0, 0, 0, 0}, // UPrime
    {0, 2, 1, 0, 0, 2, 1, 0}, // R
    {0, 0, 0, 0, 0, 0, 0, 0}, // R2
    {0, 2, 1, 0, 0, 2, 1, 0}, // RPrime
    {0, 0, 2, 1, 2, 1, 0, 0}, // F
    {0, 0, 0, 0, 0, 0, 0, 0}, // F2
    {0, 0, 2, 1, 2, 1, 0, 0}, // FPrime
    {0, 0, 0, 0, 0, 0, 0, 0}, // D
    {0, 0, 0, 0, 0, 0, 0, 0}, // D2
    {0, 0, 0, 0, 0, 0, 0, 0}, // DPrime
    {1, 0, 0, 2, 1, 0, 0, 2}, // L
    {0, 0, 0, 0, 0, 0, 0, 0}, // L2
    {1, 0, 0, 2, 1, 0, 0, 2}, // LPrime
    {2, 1, 0, 0, 0, 0, 2, 1}, // B
    {0, 0, 0, 0, 0, 0, 0, 0}, // B2
    {2, 1, 0, 0, 0, 0, 2, 1}, // BPrime
}};

constexpr std::array<std::array<int, 12>, 18> twist_e{{
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // U
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // U2
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // UPrime
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // R
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // R2
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // RPrime
    {0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0}, // F
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // F2
    {0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0}, // FPrime
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // D
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // D2
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // DPrime
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // L
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // L2
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // LPrime
    {1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0}, // B 
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // B2
    {1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0}, // BPrime
}};

struct CubeState {
    /**
     * cp[i] = j -> the corner at i slot belongs to j
     * co[i] = x -> the corner at i slot has x orientation
     */
    std::array<int, 8> cp{0, 1, 2, 3, 4, 5, 6, 7};
    std::array<int, 8> co{};
    std::array<int, 12> ep{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
    std::array<int, 12> eo{};

    constexpr CubeState() {
        cp = solved_corners;
        co = oriented_corners;
        ep = solved_edges;
        eo = oriented_edges;
    }
    
    constexpr CubeState(std::array<int, 8> cp_, std::array<int, 8> co_, std::array<int, 12> ep_, std::array<int, 12> eo_) {
        init(cp_, co_, ep_, eo_);
    }
    
    constexpr CubeState(const CubeState &other) {
        init(other.cp, other.co, other.ep, other.eo);
    }

    constexpr void init(std::array<int, 8> cp_, std::array<int, 8> co_, std::array<int, 12> ep_, std::array<int, 12> eo_) {
        cp = cp_;
        co = co_;
        ep = ep_;
        eo = eo_;
    }
    
    bool operator ==(const CubeState &other) const {
        return cp == other.cp 
            && co == other.co
            && ep == other.ep
            && eo == other.eo;
    }
};

inline CubeState apply_move(const CubeState &cube, Move mv) {
    std::array<int, 8> cp{};
    std::array<int, 8> co{};
    std::array<int, 12> ep{};
    std::array<int, 12> eo{};
    size_t move_idx = static_cast<size_t>(mv);
    for (int i = 0; i < 8; i++) {
        cp[i] = cube.cp[source_c[move_idx][i]];
        co[i] = (cube.co[source_c[move_idx][i]] + twist_c[move_idx][i]) % 3;
    }
    for (int i = 0; i < 12; i++) {
        ep[i] = cube.ep[source_e[move_idx][i]];
        eo[i] = (cube.eo[source_e[move_idx][i]] + twist_e[move_idx][i]) % 2;
    }
    return CubeState(cp, co, ep, eo);
}

/**
 * Corners all oriented
 * Edges all oriented
 * Edges 4, 5, 6, 7 are in middle (E-slice edges stay in E-slice)
 */
inline bool phase1_complete(const CubeState &cube) {
    bool ans = true;
    ans &= cube.co == oriented_corners;
    ans &= cube.eo == oriented_edges;
    for (int i = 4; i <= 7; i++) {
        ans &= (4 <= cube.ep[i] && cube.ep[i] <= 7);
    }
    return ans;
}

/**
 * Phase 1 complete
 * Corners and edges are solved
 */
inline bool phase2_complete(const CubeState &cube) {
    bool ans = true;
    ans &= phase1_complete(cube);
    ans &= cube.cp == solved_corners;
    ans &= cube.ep == solved_edges;
    return ans;
}

/**
 * Cube is solved?
 */
inline bool solved(const CubeState &cube) {
    return phase2_complete(cube);
}
}