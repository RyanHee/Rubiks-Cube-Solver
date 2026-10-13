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
            for operation in ('apply', 'phase1', 'phase2', 'solved'):
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
