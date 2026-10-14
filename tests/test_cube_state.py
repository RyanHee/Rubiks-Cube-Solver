"""Sticker validity and compatibility with the actual C++ state transitions."""

from pathlib import Path
import random
import shutil
import subprocess
import tempfile
import unittest

import numpy as np

from rubiks_cube.cube import Cube
from rubiks_cube.cube_state import CubeState, CORNER_FACELETS, EDGE_FACELETS

ROOT = Path(__file__).resolve().parents[1]
MOVES = tuple(face + suffix for face in 'URFDLB' for suffix in ('', '2', "'"))


class CubeStateTests(unittest.TestCase):
    def test_solved_and_serialization(self):
        cube = Cube()
        state = cube.to_cubestate()
        self.assertEqual(state, CubeState())
        self.assertEqual(list(map(int, state.to_solver_input().split())),
                         list(state.cp + state.co + state.ep + state.eo))
        cube.move('R')
        self.assertEqual(state, CubeState())

    def test_cpp_moves_match_sticker_conversion(self):
        compiler = shutil.which('clang++') or shutil.which('g++')
        if compiler is None:
            self.skipTest('C++ compiler unavailable')
        rng = random.Random(2026)
        # All 18 moves from solved, then a long random walk.
        ids = []
        for move in range(18):
            ids.extend((move, move - move % 3 + (2 - move % 3)))
        ids.extend(rng.randrange(18) for _ in range(500))
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / 'bridge'
            subprocess.run([compiler, '-std=c++23', '-I', str(ROOT / 'cpp/include'),
                            str(ROOT / 'tests/cpp/sticker_bridge.cpp'), '-o', str(executable)],
                           check=True, capture_output=True, text=True)
            output = subprocess.run([str(executable)], input=' '.join(map(str, ids)),
                                    check=True, capture_output=True, text=True).stdout
        cube = Cube()
        for move, line in zip(ids, output.splitlines(), strict=True):
            cube.move(MOVES[move])
            state = cube.to_cubestate()
            self.assertEqual(list(state.cp + state.co + state.ep + state.eo),
                             list(map(int, line.split())))

    def test_bad_shape_counts_colors_and_centers(self):
        with self.assertRaisesRegex(ValueError, 'shape'):
            Cube([['W']])
        with self.assertRaisesRegex(ValueError, 'shape'):
            CubeState.from_facelets([['W']])
        for color, message in [('?', 'colors'), ('G', 'nine')]:
            stickers = Cube().cube
            stickers[0, 0, 0] = color
            with self.assertRaisesRegex(ValueError, message):
                CubeState.from_facelets(stickers)
        stickers = Cube().cube
        stickers[0, 1, 1], stickers[1, 1, 1] = 'O', 'W'
        with self.assertRaisesRegex(ValueError, 'Centers'):
            CubeState.from_facelets(stickers)

    def test_impossible_positions(self):
        for kind, message in [('flip', 'Edge flips'), ('twist', 'Corner twists'),
                              ('mirror', 'mirrored corner'), ('swap', 'parity')]:
            stickers = Cube().cube
            flat = stickers.ravel()
            if kind == 'flip':
                indices = list(EDGE_FACELETS[0])
                flat[indices] = flat[indices[::-1]]
            elif kind == 'twist':
                indices = list(CORNER_FACELETS[0])
                flat[indices] = np.roll(flat[indices], 1)
            elif kind == 'mirror':
                a, b = CORNER_FACELETS[0][1:]
                flat[a], flat[b] = flat[b], flat[a]
            else:
                first, second = map(list, EDGE_FACELETS[:2])
                flat[first], flat[second] = flat[second].copy(), flat[first].copy()
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, message):
                CubeState.from_facelets(stickers)

    def test_duplicate_pieces_and_bad_arrays(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            CubeState(ep=(0,) * 12)
        with self.assertRaisesRegex(ValueError, 'co must'):
            CubeState(co=(1.5,) + (0,) * 7)
        source = list(range(8))
        state = CubeState(cp=source)
        source[0] = 7
        self.assertEqual(state.cp, tuple(range(8)))
