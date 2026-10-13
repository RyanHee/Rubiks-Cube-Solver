# PLL movement fixtures

Source: [CubeSkills PLL sheet](https://www.cubeskills.com/uploads/pdf/tutorials/pll-algorithms.pdf),
by Feliks Zemdegs and Andy Klise. Regeneration expects the optional reference at
`docs/references/pll-algorithms.pdf`; the PDF is currently absent.
All 21 cases use the bold, suggested algorithm, including the final adjustments
printed in square brackets. Parentheses only group moves.

`pll_cases.json` stores each diagram's four colored side strips and explicit
starting facelets in this project's U, L, F, R, B, D order. U is white, D is
yellow, L orange, F green, R red, and B blue. The sheet uses yellow on top and
different front colors for different cases; each diagram's color map records
the relabeling to this project's fixed centers. Back and right strips are
reversed when converting the top-down diagrams to face rows.

Tests construct each initial state directly from these stored facelets. They
never scramble a solved `Cube` with the inverse algorithm, so inverse mistakes
in `Cube.move()` cannot cancel out during setup and give false passing results.
Every test compares all 54 resulting stickers with the fixed solved state.

The model supports only outer face turns. `outer_algorithm` is the printed
algorithm expressed with R, L, U, D, F, B turns, tracking cube rotations as
changes of reference frame. For example, M = x' R L' and u = y D. A half turn
such as R2' is equivalent to R2. These tests exercise the model's outer turns;
they do not imply that `Cube.move()` supports raw slice/wide/rotation notation.

The optional generator reads colors from the PDF diagrams and cross-checks
their orientation against an independent integer-coordinate sticker simulator.
That simulator does not import the production model. Generation requires
PyMuPDF and Pillow; running the tests only needs the project's normal packages.

```sh
python tools/generate_pll_fixtures.py
python -m unittest tests.test_pll -v
```
