# Rubiks-Cube-Solver

A Python/Ursina cube visualizer with a C++ cubie-state implementation for a
planned two-phase solver. Pattern-database generation is implemented for both
phases, along with phase-1 and phase-2 IDA* search. Database persistence is not
implemented yet.

## Project layout

```text
main.py                       # Python app launcher
rubiks_cube/                  # Python model and visualizer application
cpp/include/rubiks/           # C++ solver headers
assets/textures/              # Sticker textures and original color images
data/                         # Corner/edge mappings and initial cube state
docs/mapping_rules.txt        # Custom sticker-lettering conventions
docs/references/              # Reference download instructions and optional PDFs
tests/                        # Active movement and PLL regression tests
  fixtures/                   # Explicit PLL starting states
  reference/                  # Inactive tests for the removed Python state class
tools/                        # Mapping inspection and asset/fixture generators
.vscode/settings.json         # VS Code unittest discovery configuration
```

## Setup and run

From the project root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ursina numpy
python main.py
```

Alternatively, run `python -m rubiks_cube`. The intro screen offers Simulator
and Solver / Sticker Input modes. The simulator initially loads facelets from
`data/cube_init.txt` in U, L, F, R, B, D order. The application resolves data and
texture paths relative to the project, independent of the working directory.

On macOS, the visualizer uses an OpenGL core context, GLSL 150 shaders, and
standard alpha blending for the UI.

## Controls

| Turn | Clockwise | Prime |
|---|---|---|
| R | r | t |
| L | l | ; |
| U | u | i |
| D | d | s |
| F | f | g |
| B | b | n |

Hold the right mouse button and drag to orbit; scroll to zoom; middle-drag to
pan. Perspective zoom is limited to 6–40 units.

## Tests

```sh
python -m unittest discover -s tests -t . -v
python -m unittest tests.test_pll -v
```

VS Code's Testing sidebar is configured to discover the active tests in
`tests/`. Refresh the sidebar after changing the layout.

The 21 PLL cases come from the [CubeSkills sheet](https://www.cubeskills.com/uploads/pdf/tutorials/pll-algorithms.pdf).
Each test starts from explicit diagram facelets and applies the solving
algorithm. See [fixture documentation](tests/fixtures/README.md) for provenance
and notation details. The previous Python cubie-state tests are preserved in
`tests/reference/` and are not discovered because their implementation was removed.

## C++ state

Include `rubiks/cube_state.hpp`, using `cpp/include` as an include directory
and C++20 or later:

`compile_flags.txt` supplies the same language version and include path to
clangd-based editors such as Zed. Open the project root folder in the editor.

```sh
c++ -std=c++20 -I cpp/include your_program.cpp -o your_program
```

The custom piece numbering is defined in `data/corner_mapping.json` and
`data/edge_mapping.json`; its conventions are in [mapping rules](docs/mapping_rules.txt).

`rubiks::generate_tables()` in `rubiks/table.hpp` generates all four pattern
databases in memory. The existing `corner_distance` and `edge_distance` fields
are for phase 1; `phase2_corner_distance` and `phase2_edge_distance` are for
phase 2. Phase-2 tables have 967,680 entries each and use the 10 restricted moves.

After `phase1_complete(cube)` is true, access their distances with:

```cpp
int corner_distance = tables.phase2_corner_distance[cube.phase2_state_corners()];
int edge_distance = tables.phase2_edge_distance[cube.phase2_state_edges()];
```

The phase-2 indices combine a lexicographic 8-piece permutation rank with the
4-piece slice permutation rank: `permutation * 24 + slice`. Slice pieces are
IDs 4–7; U/D edges are IDs 0–3 and 8–11. The solved indices are zero. Table
generation is runtime work; saving/loading the databases is not implemented yet.

Phase-1 search is declared in `rubiks/solver.hpp` and implemented in
`cpp/src/solver.cpp`. `phase1(root)` returns moves reaching the phase-2 subgroup,
leaves `root` unchanged, and returns an empty path if phase 1 is already complete.
The search starts at the pattern-database lower bound and searches up to 12 moves.
`phase2(endpoint)` uses the same search structure with phase-2 heuristics, the
10 restricted moves, a fully solved goal, and an 18-move cap. It rejects inputs
outside the subgroup with `std::invalid_argument`. Both phases leave input
states unchanged and throw `std::runtime_error` if their move limit is exhausted.

The standalone executable reads 40 cubie integers (8 cp, 8 co, 12 ep, 12 eo),
runs phase 1 followed by phase 2, and prints space-separated solution moves.
This initial approach uses the first phase-1 solution; it does not optimize
the combined solution length or implement a search timeout.

## Development tools

```sh
python tools/inspect_mappings.py
python tools/create_stickers.py
python tools/generate_pll_fixtures.py
```

The sticker tool rewrites the letter-named sticker textures. The PLL fixture
generator requires the optional `docs/references/pll-algorithms.pdf`, which is
currently absent. See [reference instructions](docs/references/README.md).
It also requires PyMuPDF and Pillow (`python -m pip install pymupdf pillow`).

### Python sticker validation and solver state

Use `cube.to_cubestate()` (or `CubeState.from_facelets(stickers)` from
`rubiks_cube.cube_state`) to validate sticker input and create immutable
`cp`, `co`, `ep`, and `eo` tuples matching the C++ solver. Input has shape
`(6, 3, 3)` in U, L, F, R, B, D order, with each face viewed from outside.
Centers must be W, O, G, R, B, Y respectively.

```python
from rubiks_cube.cube import Cube

cube = Cube()
cube.move('R')
try:
    state = cube.to_cubestate()
except ValueError as error:
    print(error)  # Can be displayed by the future sticker-input GUI.
else:
    solver_input = state.to_solver_input()  # 40 integers for the C++ CLI.
```

Validation rejects incorrect colors/counts/centers, invalid or mirrored pieces,
duplicate pieces, impossible twists/flips, and mismatched permutation parity.
Conversion snapshots the input and does not change the simulator cube.

### GUI modes and sticker entry

The app opens on a mode selection screen. Choose **Simulator** for the existing
3D controls, or **Solver / Sticker Input** to edit an unfolded cube net. Select
one of the six paint colors and click stickers; center stickers are locked.
Each paint button shows its current count out of nine.

Use **Prev / Next** to choose from 10 palettes: Classic, Bright, Pastel, Muted,
Ocean, Neon, Earth, Candy, Jewel, and High contrast. These change the displayed
colors while retaining the W/O/G/R/B/Y piece identities.

**Validate cube** checks physical reachability. On success, **Open in simulator**
shows the entered cube in 3D with the chosen palette. Sticker edits persist when
switching modes. Use **Modes** or Escape to return to the intro screen.
Click **Solve cube** to validate the stickers and run the C++ two-phase solver.
The app builds `build/rubiks_solver` automatically on first use or after changes
to C++ sources/headers. A C++23 compiler is required (`clang++`, `g++`, or `c++`);
on macOS install Xcode Command Line Tools if needed.

Compiling and searching run in a separate process, keeping the GUI responsive.
Use **Cancel solve** or switch modes to stop a search. Searches have a 120-second
timeout; difficult cubes can exceed it with the current search implementation.
Pattern databases are still generated each time the solver process starts.

The returned moves are verified against the Python sticker model. The solution
screen supports **Play/Pause**, **Next move**, **Restart**, and **Edit stickers**.
Orbit and zoom remain available; manual face turns are disabled during solution
playback to keep the displayed cube aligned with the solution. Restart restores
the original entered cube.

During solution playback, use the **− / +** speed controls to choose **0.25× to
4×** speed. Changes take effect on the next move. A curved gold arrow marks the
turning face and its direction, viewed from outside that face; half turns show
an extended 180-degree arc. Orbit the cube to see arrows on rear-facing faces.
