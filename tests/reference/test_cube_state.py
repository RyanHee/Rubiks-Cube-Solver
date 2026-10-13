"""Verify graph states against the independent facelet movement model."""

from collections import deque
from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import random
import unittest

import numpy as np

from cube_state import CubeState, CORNER_FACELETS, EDGE_FACELETS, MOVES
from rubiks_cube.cube import Cube


class CubeStateTests(unittest.TestCase):
    def test_solved_cube_round_trip(self):
        cube = Cube()
        state = CubeState.from_cube(cube)
        self.assertEqual(state, CubeState())
        self.assertTrue(state.is_solved())
        np.testing.assert_array_equal(state.to_facelets(), cube.cube)

    def test_all_18_moves_match_facelet_model(self):
        for move in MOVES:
            with self.subTest(move=move):
                cube = Cube()
                cube.move(move)
                state = CubeState().moved(move)
                self.assertEqual(CubeState.from_cube(cube), state)
                np.testing.assert_array_equal(state.to_facelets(), cube.cube)

    def test_sequential_scramble_matches_at_every_move(self):
        randomizer = random.Random(2026)
        cube = Cube()
        state = CubeState()
        for index in range(100):
            move = randomizer.choice(MOVES)
            with self.subTest(index=index, move=move):
                cube.move(move)
                state = state.moved(move)
                self.assertEqual(CubeState.from_cube(cube), state)
                np.testing.assert_array_equal(state.to_facelets(), cube.cube)

    def test_all_pll_states_round_trip_and_solve(self):
        path = Path(__file__).resolve().parents[1] / 'fixtures/pll_cases.json'
        fixtures = json.loads(path.read_text())
        for case in fixtures['cases']:
            with self.subTest(case=case['name']):
                facelets = np.array([
                    [list(row) for row in case['initial_faces'][face]]
                    for face in fixtures['face_order']
                ])
                state = CubeState.from_facelets(facelets)
                np.testing.assert_array_equal(state.to_facelets(), facelets)
                for move in case['outer_algorithm'].split():
                    state = state.moved(move)
                self.assertEqual(state, CubeState())

    def test_move_does_not_mutate_parent_node(self):
        parent = CubeState()
        child = parent.moved('R')
        self.assertTrue(parent.is_solved())
        self.assertFalse(child.is_solved())
        with self.assertRaises(FrozenInstanceError):
            parent.cp = child.cp

    def test_input_arrays_do_not_alias_state(self):
        facelets = Cube().cube
        state = CubeState.from_facelets(facelets)
        facelets[0, 0, 0] = 'G'
        returned = state.to_facelets()
        returned[0, 0, 0] = 'R'
        self.assertEqual(state, CubeState())

    def test_constructor_copies_mutable_arrays(self):
        corners = list(range(8))
        state = CubeState(cp=corners)
        corners[0] = 7
        self.assertEqual(state.cp, tuple(range(8)))
        self.assertIsInstance(hash(state), int)

    def test_neighbors_are_18_distinct_labeled_edges(self):
        edges = list(CubeState().neighbors())
        self.assertEqual(tuple(move for move, _ in edges), MOVES)
        self.assertEqual(len({state.key() for _, state in edges}), 18)
        self.assertTrue(all(len(state.key()) == 40 for _, state in edges))

    def test_short_scramble_is_a_graph_path_to_the_goal(self):
        start = CubeState().moved('R').moved('U2')
        queue = deque([(start, [])])
        visited = {start.key()}
        solution = None
        while queue:
            state, path = queue.popleft()
            if state.is_solved():
                solution = path
                break
            if len(path) == 2:
                continue
            for move, child in state.neighbors():
                if child.key() not in visited:
                    visited.add(child.key())
                    queue.append((child, path + [move]))
        self.assertEqual(solution, ['U2', "R'"])

    def test_color_labels_are_normalized_by_fixed_centers(self):
        colors = ('white', 'orange', 'green', 'red', 'blue', 'yellow')
        labeled = CubeState(centers=colors).moved('F')
        restored = CubeState.from_facelets(labeled.to_facelets())
        self.assertEqual(restored, labeled)
        self.assertEqual(restored.key(), CubeState().moved('F').key())

    def test_invalid_shape_and_color_counts_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'shape'):
            CubeState.from_facelets(np.zeros((54,)))
        facelets = Cube().cube
        facelets[0, 0, 0] = 'G'
        with self.assertRaisesRegex(ValueError, 'nine'):
            CubeState.from_facelets(facelets)

    def test_duplicate_center_colors_are_rejected(self):
        facelets = Cube().cube
        facelets[1, 1, 1] = 'W'
        with self.assertRaisesRegex(ValueError, 'distinct'):
            CubeState.from_facelets(facelets)

    def test_single_flipped_edge_is_rejected(self):
        facelets = Cube().cube
        flat = facelets.ravel()
        a, b = EDGE_FACELETS[0]
        flat[a], flat[b] = flat[b], flat[a]
        with self.assertRaisesRegex(ValueError, 'edge flips'):
            CubeState.from_facelets(facelets)

    def test_single_twisted_corner_is_rejected(self):
        facelets = Cube().cube
        flat = facelets.ravel()
        a, b, c = CORNER_FACELETS[0]
        flat[a], flat[b], flat[c] = flat[c], flat[a], flat[b]
        with self.assertRaisesRegex(ValueError, 'corner twists'):
            CubeState.from_facelets(facelets)

    def test_mirrored_corner_is_rejected(self):
        facelets = Cube().cube
        flat = facelets.ravel()
        _, a, b = CORNER_FACELETS[0]
        flat[a], flat[b] = flat[b], flat[a]
        with self.assertRaisesRegex(ValueError, 'mirrored corner'):
            CubeState.from_facelets(facelets)

    def test_single_edge_swap_is_rejected(self):
        facelets = Cube().cube
        flat = facelets.ravel()
        first, second = EDGE_FACELETS[:2]
        flat[list(first)], flat[list(second)] = flat[list(second)].copy(), flat[list(first)].copy()
        with self.assertRaisesRegex(ValueError, 'parity'):
            CubeState.from_facelets(facelets)

    def test_duplicate_cubies_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate pieces'):
            CubeState(ep=(0,) * 12)

    def test_invalid_orientation_values_are_rejected(self):
        for invalid in (3, -1, 1.5):
            with self.subTest(value=invalid):
                with self.assertRaisesRegex(ValueError, 'co must'):
                    CubeState(co=(invalid,) + (0,) * 7)

    def test_unknown_moves_are_rejected(self):
        for move in ('M', 'x', 'r', '', 'R3', 'Q'):
            with self.subTest(move=move):
                with self.assertRaisesRegex(ValueError, 'Unsupported move'):
                    CubeState().moved(move)


if __name__ == '__main__':
    unittest.main()
