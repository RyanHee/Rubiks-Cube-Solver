#pragma once

#include "rubiks/slice_mapping.hpp"
#include <array>
#include <cassert>
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

inline constexpr std::array<Move, 18> phase1_moves{
    Move::U, Move::U2, Move::UPrime,
    Move::R, Move::R2, Move::RPrime,
    Move::F, Move::F2, Move::FPrime,
    Move::D, Move::D2, Move::DPrime,
    Move::L, Move::L2, Move::LPrime,
    Move::B, Move::B2, Move::BPrime
};

inline constexpr std::array<Move, 10> phase2_moves{
    Move::U, Move::U2, Move::UPrime,
    Move::R2, Move::F2,
    Move::D, Move::D2, Move::DPrime,
    Move::L2, Move::B2
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

struct CubeState;
inline void assert_valid_cube(const CubeState &cube);

struct CubeState {
    /**
     * cp[i] = j -> the corner at i slot belongs to j
     * co[i] = x -> the corner at i slot has x orientation
     */
    std::array<int, 8> cp{0, 1, 2, 3, 4, 5, 6, 7};
    std::array<int, 8> co{};
    std::array<int, 12> ep{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
    std::array<int, 12> eo{};
    int twist{};
    int flip{};
    int slice_mask{};

    constexpr CubeState() {
        init(solved_corners, oriented_corners, solved_edges, oriented_edges);
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
        twist = 0;
        flip = 0;
        slice_mask = 0;
        for (int i = 0; i < 7; i++) {
            twist = twist * 3 + co[i];
        }
        for (int i = 0; i < 12; i++) {
            if (i < 11) {
                flip = flip * 2 + eo[i];
            }
            if (4 <= ep[i] && ep[i] <= 7) {
                slice_mask |= 1 << i;
            }
        }
    }
    
    bool operator ==(const CubeState &other) const {
        return cp == other.cp 
            && co == other.co
            && ep == other.ep
            && eo == other.eo;
    }

    int phase1_state_corners() const {
        assert_valid_cube(*this);
        assert(twist >= 0 && twist < 2187 && "invalid corner orientation coordinate");
        assert(slice_mask >= 0 && slice_mask < 4096 && "invalid slice mask");
        const int slice = slice_mapping.coordinate[slice_mask];
        assert(slice >= 0 && "slice mask must contain exactly four positions");
        return twist * 495 + slice;
    }

    int phase1_state_edges() const {
        assert_valid_cube(*this);
        assert(flip >= 0 && flip < 2048 && "invalid edge orientation coordinate");
        assert(slice_mask >= 0 && slice_mask < 4096 && "invalid slice mask");
        const int slice = slice_mapping.coordinate[slice_mask];
        assert(slice >= 0 && "slice mask must contain exactly four positions");
        return flip * 495 + slice;
    }
};

// Debug preconditions for a physically reachable cubie state. Array lengths
// are already enforced by std::array. These checks disappear with NDEBUG.
inline void assert_valid_cube([[maybe_unused]] const CubeState &cube) {
#ifndef NDEBUG
    std::array<bool, 8> seen_corners{};
    std::array<bool, 12> seen_edges{};
    int corner_twists = 0;
    int edge_flips = 0;
    int corner_parity = 0;
    int edge_parity = 0;
    for (std::size_t i = 0; i < cube.cp.size(); ++i) {
        assert(cube.cp[i] >= 0 && cube.cp[i] < 8 && "cp entries must be in 0..7");
        assert(!seen_corners[cube.cp[i]] && "cp must contain each corner exactly once");
        seen_corners[cube.cp[i]] = true;
        assert(cube.co[i] >= 0 && cube.co[i] < 3 && "co entries must be in 0..2");
        corner_twists += cube.co[i];
        for (std::size_t j = i + 1; j < cube.cp.size(); ++j) {
            corner_parity ^= cube.cp[i] > cube.cp[j];
        }
    }
    for (std::size_t i = 0; i < cube.ep.size(); ++i) {
        assert(cube.ep[i] >= 0 && cube.ep[i] < 12 && "ep entries must be in 0..11");
        assert(!seen_edges[cube.ep[i]] && "ep must contain each edge exactly once");
        seen_edges[cube.ep[i]] = true;
        assert(cube.eo[i] >= 0 && cube.eo[i] < 2 && "eo entries must be in 0..1");
        edge_flips += cube.eo[i];
        for (std::size_t j = i + 1; j < cube.ep.size(); ++j) {
            edge_parity ^= cube.ep[i] > cube.ep[j];
        }
    }
    assert(corner_twists % 3 == 0 && "corner twists must sum to 0 modulo 3");
    assert(edge_flips % 2 == 0 && "edge flips must sum to 0 modulo 2");
    assert(corner_parity == edge_parity && "corner and edge permutation parity must match");
#endif
}

inline CubeState apply_move(const CubeState &cube, Move mv) {
    assert_valid_cube(cube);
    assert(static_cast<int>(mv) >= 0 && static_cast<int>(mv) < 18 && "invalid Move value");
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
    assert_valid_cube(cube);
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
    assert_valid_cube(cube);
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
    assert_valid_cube(cube);
    return phase2_complete(cube);
}

constexpr CubeState solved_cube(solved_corners, oriented_corners, solved_edges, oriented_edges);
}
