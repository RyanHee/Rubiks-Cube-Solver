# Rubiks-Cube-Solver
_solver is not implemented yet_

## Requirements
pip install ursina  
pip install numpy

# Run
run main.py

On macOS, the visualizer requests an OpenGL core context and uses GLSL 150
for the cube, sky, and UI shaders. Restart the app after updating the code.

# Controls
r and t for right moves  
l and ; for left moves  
u and i for top layer moves  
s and d for bottom layer moves  
f and g for front layer moves  
b and n for back layer moves

## Movement tests

Run the 21 PLL cases from the [CubeSkills algorithm sheet](https://www.cubeskills.com/uploads/pdf/tutorials/pll-algorithms.pdf):

```sh
python -m unittest test_pll -v
```

Each test starts from explicit diagram facelets and checks that the solving
algorithm produces a fully solved cube. Fixture provenance and notation details
are in [tests/fixtures/README.md](tests/fixtures/README.md).

## Solver graph representation

`CubeState` in `cube_state.py` represents a graph node using eight corners and
twelve edges, each with a position and orientation. It is immutable and
hashable. The solved node has every piece in its home position with orientation
zero. Each of the 18 outer-face moves is a unit-cost edge; `R2` counts as one.
The graph is generated on demand rather than stored in memory.

```python
from Rubiks_Cube import Cube
from cube_state import CubeState

cube = Cube()
cube.move('R')
state = CubeState.from_cube(cube)

next_state = state.moved("R'")  # state itself stays unchanged
assert next_state.is_solved()

for move, neighbor in state.neighbors():
    visited_key = neighbor.key()

facelets = state.to_facelets()  # shape (6, 3, 3), ordered U L F R B D
```

`CubeState.from_facelets()` validates color counts, cubie identities, orientation
constraints, and permutation parity before accepting user input. The graph
state module can run without loading Ursina. This is the representation layer;
two-phase search and pattern databases are still to be implemented.
