# Rubiks-Cube-Solver

An interactive 3×3 Rubik's Cube simulator and solver, presented as **Cube
Studio**. The Python/Ursina app provides a 3D simulator, a sticker editor with
physical-state validation, and animated solution playback. A C++ two-phase
solver uses pattern databases and IDA* search to find the moves.

## Setup and run

Run these commands from the project root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ursina numpy
python main.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.
You can also launch the app with `python -m rubiks_cube`.

The desktop app requires a graphical display. Solving also requires a compiler
with C++23 support, available as `clang++`, `g++`, or `c++`. On macOS, install
Xcode Command Line Tools with `xcode-select --install` if needed. The app builds
`build/rubiks_solver` automatically on the first solve and rebuilds it when C++
sources or headers change.

Data and textures resolve relative to the project, independent of the working
directory. On macOS, the visualizer uses an OpenGL core context, GLSL 150
shaders, and standard alpha blending for the UI.

## Using the app

The opening screen offers two modes:

- **Simulator**: turn and inspect the 3D cube. Its initial stickers come from
  `data/cube_init.txt`, in U, L, F, R, B, D order.
- **Solver / Sticker Input**: enter a cube on an unfolded net. Select a paint
  color and click stickers; centers are locked, and each color shows its count
  out of nine. Keep white up and green in front, with each face viewed from
  outside.

In the sticker editor, **Validate cube** checks whether the cube is physically
reachable. After validation, **Open in simulator** previews it in 3D.
**Solve cube** validates the input and runs the C++ solver. **Reset to solved**
clears the entered state. Sticker edits persist when switching modes.

Use the palette **Prev / Next** buttons to choose from 10 palettes: Classic,
Bright, Pastel, Muted, Ocean, Neon, Earth, Candy, Jewel, and High contrast.
Palettes change the display colors while preserving W/O/G/R/B/Y identities.
Use **Modes** or Escape to return to the opening screen.

Compiling and searching run in child processes to keep the GUI responsive.
Use **Cancel solve** or switch modes to stop a search. The bridge applies a
120-second timeout to each build/search stage. Difficult cubes can exceed the
search timeout; pattern databases are generated every time the solver starts.

Returned moves are checked against the Python sticker model before playback.
The solution screen offers **Play/Pause**, **Next move**, **Restart**, and
**Edit stickers**. Restart restores the entered cube. The **− / +** controls
select speeds from **0.25× to 4×**, taking effect on the next move. A curved gold
arrow marks the turning face and direction; half turns show a 180-degree arc.
Orbit to see arrows on rear-facing faces. Orbit and zoom remain available
during playback, while manual face turns are disabled.

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

The suite covers Python face turns, sticker validation, all 21 PLL cases,
C++ state assertions and search, and the Python-to-C++ solver bridge. Run it
with the Python dependencies installed and a C++23 compiler available; the
bridge tests build the solver when needed.

The 21 PLL cases come from the [CubeSkills sheet](https://www.cubeskills.com/uploads/pdf/tutorials/pll-algorithms.pdf).
Each test starts from explicit diagram facelets and applies the solving
algorithm. See [fixture documentation](tests/fixtures/README.md) for provenance
and notation details. Tests for the earlier Python cubie-state representation are preserved in
`tests/reference/`. That directory is excluded from normal unittest discovery;
the current sticker-to-cubie bridge is tested in `tests/test_cube_state.py`.

## C++ state

Include `rubiks/cube_state.hpp`, using `cpp/include` as an include directory
and C++23 for the full solver:

`compile_flags.txt` supplies the same language version and include path to
clangd-based editors such as Zed. Open the project root folder in the editor.

```sh
c++ -std=c++23 -I cpp/include your_program.cpp -o your_program
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

To build and run the standalone solver manually:

```sh
mkdir -p build
c++ -std=c++23 -O3 -DNDEBUG -I cpp/include cpp/src/solver.cpp -o build/rubiks_solver
python - <<'PYTHON'
from pathlib import Path
from rubiks_cube.cube import Cube

cube = Cube()
for move in ("R", "U", "F2"):
    cube.move(move)
Path("build/cube.txt").write_text(cube.to_cubestate().to_solver_input())
PYTHON
./build/rubiks_solver build/cube.txt
```

The executable takes a cube-file path as its only argument. The file contains
40 cubie integers (8 cp, 8 co, 12 ep, 12 eo). The solver runs phase 1 followed
by phase 2 and prints space-separated solution moves.
This initial approach uses the first phase-1 solution; it does not optimize
the combined solution length or implement a CLI search timeout. The GUI bridge
enforces its own timeout.

## Development tools

```sh
python tools/inspect_mappings.py
python tools/create_stickers.py
python tools/generate_pll_fixtures.py
```

The sticker tool requires Pillow (`python -m pip install pillow`) and rewrites
the letter-named sticker textures. The PLL fixture generator requires the optional `docs/references/pll-algorithms.pdf`, which is
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
    print(error)
else:
    solver_input = state.to_solver_input()  # 40 integers for the C++ CLI.
```

Validation rejects incorrect colors/counts/centers, invalid or mirrored pieces,
duplicate pieces, impossible twists/flips, and mismatched permutation parity.
Conversion snapshots the input and does not change the simulator cube.

## Project layout

```text
main.py                       # Python app launcher
rubiks_cube/                  # Python model and visualizer application
cpp/include/rubiks/           # C++ state, tables, and solver headers
cpp/src/solver.cpp            # Two-phase search and standalone CLI
assets/textures/              # Sticker textures and original color images
data/                         # Corner/edge mappings and initial cube state
docs/mapping_rules.txt        # Custom sticker-lettering conventions
docs/references/              # Reference download instructions and optional PDFs
tests/                        # Python, C++, PLL, and solver bridge tests
  fixtures/                   # Explicit PLL starting states
  reference/                  # Inactive tests for the removed Python state class
tools/                        # Mapping inspection and asset/fixture generators
.vscode/settings.json         # VS Code unittest discovery configuration
```
