"""Exercise the actual Python -> C++ CLI -> sticker solution bridge."""
import time
import unittest

from rubiks_cube.cube import Cube
from rubiks_cube.cube_state import CubeState
from rubiks_cube.solver import SolverJob


class SolverBridgeTests(unittest.TestCase):
    def solve(self, cube):
        job = SolverJob(cube.to_cubestate(), timeout=30)
        try:
            deadline = time.monotonic() + 40
            while not job.done and time.monotonic() < deadline:
                job.poll()
                time.sleep(.01)
            self.assertTrue(job.done, 'Solver did not finish')
            self.assertIsNone(job.error)
            return job.result
        finally:
            job.close()

    def test_mixed_scramble_returns_solution(self):
        cube = Cube()
        for move in ('U', 'R2', 'F2', 'D', 'L2', 'R'):
            cube.move(move)
        before = cube.cube.copy()
        moves = self.solve(cube)
        self.assertTrue(moves)
        self.assertTrue((cube.cube == before).all())
        for move in moves:
            cube.move(move)
        self.assertEqual(cube.to_cubestate(), CubeState())

    def test_solved_cube_returns_empty_solution(self):
        self.assertEqual(self.solve(Cube()), ())

    def test_cancel_stops_process_and_releases_files(self):
        job = SolverJob(CubeState())
        directory = job.directory
        job.cancel()
        self.assertTrue(job.done)
        self.assertEqual(job.error, 'Solve cancelled.')
        if job.process is not None:
            self.assertIsNotNone(job.process.poll())
        self.assertFalse(directory.exists())
        job.poll()
        job.close()
