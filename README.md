# Rubiks-Cube-Solver

A Python/Ursina cube visualizer with a C++ cubie-state implementation for a
planned two-phase solver. Search and pattern databases are not implemented yet.

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

Alternatively, run `python -m rubiks_cube`. Initial facelets are loaded from
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
