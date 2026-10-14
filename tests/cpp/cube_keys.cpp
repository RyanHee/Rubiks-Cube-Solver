#include "rubiks/cube_state.hpp"
#include <stdexcept>
#include <unordered_set>

void require(bool condition) {
    if (!condition) throw std::runtime_error("Cube key check failed");
}

struct ConstantHash {
    std::size_t operator()(const rubiks::CubeKey&) const noexcept { return 0; }
};

int main() {
    using namespace rubiks;
    const CubeState initial;
    const auto initial_key = make_key(initial);
    const CubeState copied(initial);
    require(initial_key == make_key(copied));
    require(CubeKeyHash{}(initial_key) == CubeKeyHash{}(make_key(copied)));
    for (std::size_t i = 0; i < 8; ++i) {
        require(initial_key[i] == initial.cp[i]);
        require(initial_key[8+i] == initial.co[i]);
    }
    for (std::size_t i = 0; i < 12; ++i) {
        require(initial_key[16+i] == initial.ep[i]);
        require(initial_key[28+i] == initial.eo[i]);
    }

    std::unordered_set<CubeKey, CubeKeyHash> path;
    require(path.insert(initial_key).second);
    require(!path.insert(initial_key).second);
    const auto child = apply_move(initial, Move::R);
    const auto child_key = make_key(child);
    require(path.insert(child_key).second);
    require(make_key(apply_move(child, Move::RPrime)) == initial_key);
    require(path.erase(child_key) == 1 && path.contains(initial_key));

    // Each of the four fields must contribute to identity independently.
    auto cp = solved_corners;
    cp[0] = 1; cp[1] = 2; cp[2] = 0; // Even cycle preserves legal parity.
    require(make_key(CubeState(cp, oriented_corners, solved_edges, oriented_edges)) != initial_key);
    auto co = oriented_corners;
    co[0] = 1; co[1] = 2;
    require(make_key(CubeState(solved_corners, co, solved_edges, oriented_edges)) != initial_key);
    auto ep = solved_edges;
    ep[0] = 1; ep[1] = 2; ep[2] = 0;
    require(make_key(CubeState(solved_corners, oriented_corners, ep, oriented_edges)) != initial_key);
    auto eo = oriented_edges;
    eo[0] = 1; eo[1] = 1;
    require(make_key(CubeState(solved_corners, oriented_corners, solved_edges, eo)) != initial_key);

    std::unordered_set<CubeKey, CubeKeyHash> neighbors;
    for (Move move : phase1_moves) require(neighbors.insert(make_key(apply_move(initial, move))).second);
    require(neighbors.size() == 18);

    // Equality still distinguishes positions when every hash collides.
    std::unordered_set<CubeKey, ConstantHash> collisions;
    collisions.insert(initial_key);
    collisions.insert(child_key);
    require(collisions.size() == 2);
}
