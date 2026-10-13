# Reference tests

`test_cube_state.py` tested the earlier Python `cube_state.py` representation.
That implementation has been removed as development moves to the C++ header
in `cpp/include/rubiks/cube_state.hpp`.

This file is preserved as a reference for porting conversion and validation
tests to C++. This directory intentionally has no `__init__.py`, so unittest
does not discover these inactive tests as part of the normal test suite.
