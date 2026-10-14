"""Run C++ debug-precondition checks in isolated subprocesses."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
COMPILER = shutil.which('c++') or shutil.which('g++')


@unittest.skipUnless(COMPILER, 'A C++20 compiler is required')
class CppAssertionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.debug = Path(cls.temp.name) / 'debug_checks'
        cls.release = Path(cls.temp.name) / 'release_checks'
        for executable, flags in ((cls.debug, []), (cls.release, ['-DNDEBUG'])):
            subprocess.run([
                COMPILER, '-std=c++20', *flags,
                '-I', str(ROOT / 'cpp/include'),
                str(ROOT / 'tests/cpp/cube_assertions.cpp'),
                '-o', str(executable),
            ], check=True, capture_output=True, text=True)

    def test_valid_moves_and_predicates_in_debug_and_release(self):
        for executable in (self.debug, self.release):
            with self.subTest(build=executable.name):
                subprocess.run([str(executable)], check=True, capture_output=True)

    def test_cube_keys_and_visited_state_sets(self):
        executable = Path(self.temp.name) / 'cube_keys'
        subprocess.run([
            COMPILER, '-std=c++23', '-I', str(ROOT / 'cpp/include'),
            str(ROOT / 'tests/cpp/cube_keys.cpp'), '-o', str(executable),
        ], check=True, capture_output=True, text=True)
        subprocess.run([str(executable)], check=True, capture_output=True)

    def test_phase1_coordinate_mapping_and_boundaries(self):
        executable = Path(self.temp.name) / 'phase1_coordinates'
        subprocess.run([
            COMPILER, '-std=c++23', '-I', str(ROOT / 'cpp/include'),
            str(ROOT / 'tests/cpp/phase1_coordinates.cpp'), '-o', str(executable),
        ], check=True, capture_output=True, text=True)
        subprocess.run([str(executable)], check=True, capture_output=True)

    def test_phase2_coordinates_and_generated_tables(self):
        executable = Path(self.temp.name) / 'phase2_tables'
        subprocess.run([
            COMPILER, '-std=c++23', '-O2', '-DNDEBUG',
            '-I', str(ROOT / 'cpp/include'),
            str(ROOT / 'tests/cpp/phase2_tables.cpp'), '-o', str(executable),
        ], check=True, capture_output=True, text=True)
        subprocess.run([str(executable)], check=True, capture_output=True, timeout=60)

    def test_phase1_search(self):
        executable = Path(self.temp.name) / 'phase1_search'
        subprocess.run([
            COMPILER, '-std=c++23', '-O2', '-DNDEBUG', '-DRUBIKS_SOLVER_NO_MAIN',
            '-I', str(ROOT / 'cpp/include'),
            str(ROOT / 'cpp/src/solver.cpp'), str(ROOT / 'tests/cpp/phase1_search.cpp'),
            '-o', str(executable),
        ], check=True, capture_output=True, text=True)
        subprocess.run([str(executable)], check=True, capture_output=True, timeout=60)

    def test_phase2_search_and_two_phase_integration(self):
        executable = Path(self.temp.name) / 'phase2_search'
        subprocess.run([
            COMPILER, '-std=c++23', '-O2', '-DNDEBUG', '-DRUBIKS_SOLVER_NO_MAIN',
            '-I', str(ROOT / 'cpp/include'),
            str(ROOT / 'cpp/src/solver.cpp'), str(ROOT / 'tests/cpp/phase2_search.cpp'),
            '-o', str(executable),
        ], check=True, capture_output=True, text=True)
        subprocess.run([str(executable)], check=True, capture_output=True, timeout=60)

    def test_phase2_coordinates_require_phase1_complete(self):
        for operation in ('phase2_corners', 'phase2_edges'):
            with self.subTest(operation=operation):
                result = subprocess.run(
                    [str(self.debug), 'phase1_incomplete', operation],
                    capture_output=True, text=True,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('phase-2 coordinates require phase 1 complete', result.stderr)

    def test_invalid_arrays_are_rejected_before_each_operation(self):
        cases = {
            'cp_low': 'cp entries', 'cp_high': 'cp entries',
            'cp_duplicate': 'each corner',
            'ep_low': 'ep entries', 'ep_high': 'ep entries',
            'ep_duplicate': 'each edge',
            'co_low': 'co entries', 'co_high': 'co entries',
            'eo_low': 'eo entries', 'eo_high': 'eo entries',
            'twist_sum': 'corner twists', 'flip_sum': 'edge flips',
            'parity': 'permutation parity',
        }
        for case, message in cases.items():
            for operation in ('apply', 'phase1', 'phase2', 'solved', 'phase2_corners', 'phase2_edges'):
                with self.subTest(case=case, operation=operation):
                    result = subprocess.run(
                        [str(self.debug), case, operation],
                        capture_output=True, text=True,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(message, result.stderr)

    def test_invalid_moves_are_rejected_before_table_indexing(self):
        for case in ('move_low', 'move_high'):
            with self.subTest(case=case):
                result = subprocess.run(
                    [str(self.debug), case], capture_output=True, text=True,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('invalid Move value', result.stderr)
