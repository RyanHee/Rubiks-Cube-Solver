#pragma once

#include <array>
#include <bit>
namespace rubiks {

struct SliceMapping {
    std::array<int, 495> masks;
    std::array<int, 4096> coordinate;
};

consteval SliceMapping generate_mappings() {
    int k = 0;
    SliceMapping ans{};
    ans.coordinate.fill(-1);
    for (unsigned mask = 0; mask < 4096; mask++) {
        if (std::popcount(mask) == 4) {
            ans.masks[k] = mask;
            ans.coordinate[mask] = k++;
        }
    }
    return ans;
}

inline constexpr SliceMapping slice_mapping = generate_mappings();
}
