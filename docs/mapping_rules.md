# Sticker lettering and cubie mappings

The Python sticker model and C++ solver share the custom piece IDs defined in
[`corner_mapping.json`](../data/corner_mapping.json) and
[`edge_mapping.json`](../data/edge_mapping.json). These files define the
convention; do not substitute another solver's piece numbering.

## Face order and colors

Sticker arrays have shape `(6, 3, 3)` in this order. Each face is viewed from
outside the cube, with white up and green in front in the reference position.

| Index | Face | Color | Symbol |
|---|---|---|---|
| 0 | U | White | W |
| 1 | L | Orange | O |
| 2 | F | Green | G |
| 3 | R | Red | R |
| 4 | B | Blue | B |
| 5 | D | Yellow | Y |

The sticker editor uses this unfolded net:

```text
    U
L   F   R   B
    D
```

## Sticker letters

Corners and edges use **separate** A–X alphabets. Both assign four letters per
face, proceeding through U, L, F, R, B, D. Centers have no letter.

For corners, start at the top-left corner and proceed clockwise. For edges,
start at the top edge and proceed clockwise. The U face illustrates both:

```text
Corners       Edges
A . B         . A .
. . .         D . B
D . C         . C .
```

| Face | Corner letters clockwise from top left | Edge letters clockwise from top |
|---|---|---|
| U | A B C D | A B C D |
| L | E F G H | E F G H |
| F | I J K L | I J K L |
| R | M N O P | M N O P |
| B | Q R S T | Q R S T |
| D | U V W X | U V W X |

For example, corner A is the white sticker of the white/orange/blue corner;
corner G is the orange sticker of the orange/green/yellow corner. Edge D is
the white sticker of the white/orange edge, and edge L is the green sticker
of the orange/green edge.

## Piece IDs and orientation

Each JSON file has two objects:

- `Position` maps a group of sticker letters to its piece/slot ID. Corner IDs
  range from 0 to 7; edge IDs range from 0 to 11. For example, corner `AER`
  has ID 0, and edge `AQ` has ID 0.
- `Orientation` assigns an integer code to each sticker letter. Take the code
  modulo 3 for corners or modulo 2 for edges to get its orientation class.
  The full code is not a piece ID.

Corner class 0 corresponds to the white/yellow sticker. Edge class 0 uses the
white/yellow sticker when present, or the green/blue sticker for slice edges.
To preserve twist direction, the Python converter orders each piece's stickers
by orientation class, then matches cyclic rotations of that ordered color
sequence. See [`cube_state.py`](../rubiks_cube/cube_state.py) for the conversion.

Slice edges have IDs 4–7; U/D edges have IDs 0–3 and 8–11. This grouping is
also used by the C++ solver's phase-2 coordinates.

## Solver state

`CubeState` contains four arrays indexed by slot:

| Array | Length | Meaning |
|---|---|---|
| `cp` | 8 | Corner piece ID occupying each corner slot |
| `co` | 8 | Corner orientation, 0–2 |
| `ep` | 12 | Edge piece ID occupying each edge slot |
| `eo` | 12 | Edge orientation, 0–1 |

A solved cube has identity permutations and all-zero orientations. A reachable
state contains each piece exactly once, has corner twists summing to 0 modulo
3 and edge flips summing to 0 modulo 2, and has matching corner/edge permutation
parity. Sticker conversion also checks fixed centers, nine stickers per color,
and rejects mirrored corners.

`CubeState.to_solver_input()` serializes 40 whitespace-separated integers in
`cp`, `co`, `ep`, `eo` order for the C++ CLI. Use `Cube.to_cubestate()` or
`CubeState.from_facelets()` to validate stickers before serialization.

To inspect the JSON orientation codes:

```sh
python tools/inspect_mappings.py
```
