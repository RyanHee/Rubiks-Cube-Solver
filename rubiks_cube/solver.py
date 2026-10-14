"""Nonblocking build and subprocess bridge to the C++ two-phase solver."""
from pathlib import Path
import atexit
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
MOVES = frozenset(face + suffix for face in 'URFDLB' for suffix in ('', '2', "'"))


class SolverError(RuntimeError):
    pass


class SolverJob:
    """Poll on the UI thread; compiling and searching run in child processes."""

    def __init__(self, state, timeout=120):
        self.result = None
        self.error = None
        self.process = None
        self.stage = 'Preparing solver'
        self.timeout = timeout
        self.started = time.monotonic()
        self._temp = tempfile.TemporaryDirectory(prefix='rubiks-solver-')
        self.directory = Path(self._temp.name)
        self.binary = ROOT / 'build' / 'rubiks_solver'
        self._output = None
        self._errors = None
        self._closed = False
        atexit.register(self.close)
        (self.directory / 'cube.txt').write_text(state.to_solver_input())
        try:
            sources = [ROOT / 'cpp/src/solver.cpp', *sorted((ROOT / 'cpp/include/rubiks').glob('*.hpp'))]
            if self.binary.exists() and self.binary.stat().st_mtime >= max(p.stat().st_mtime for p in sources):
                self._search()
            else:
                compiler = shutil.which('clang++') or shutil.which('g++') or shutil.which('c++')
                if compiler is None:
                    raise SolverError('A C++23 compiler is required. Install Xcode Command Line Tools on macOS.')
                self.stage = 'Building solver (first run or source changed)'
                self._launch([compiler, '-std=c++23', '-O3', '-DNDEBUG', '-I', str(ROOT / 'cpp/include'),
                              str(sources[0]), '-o', str(self.directory / 'solver')])
        except Exception as error:
            self.error = str(error)
            self.close()

    @property
    def done(self):
        return self.result is not None or self.error is not None

    def _launch(self, command):
        self._output = (self.directory / 'stdout.txt').open('w+')
        self._errors = (self.directory / 'stderr.txt').open('w+')
        self.process = subprocess.Popen(command, stdout=self._output, stderr=self._errors)
        self.started = time.monotonic()

    def _search(self):
        self.stage = 'Solving cube'
        self._launch([str(self.binary), str(self.directory / 'cube.txt')])

    def poll(self):
        if self.done or self._closed:
            return
        try:
            code = self.process.poll()
            if code is None:
                if time.monotonic() - self.started > self.timeout:
                    raise SolverError('Search timed out. This cube needs more time than the current solver allows.')
                return
            self._output.seek(0)
            output = self._output.read()
            self._errors.seek(0)
            errors = self._errors.read()
            self._output.close()
            self._errors.close()
            if code:
                raise SolverError(f'{self.stage} failed: {errors.strip()[-1500:] or "process exited unexpectedly"}')
            if self.stage.startswith('Building'):
                self.binary.parent.mkdir(exist_ok=True)
                shutil.copy2(self.directory / 'solver', self.binary)
                self._search()
            else:
                moves = tuple(output.split())
                if any(move not in MOVES for move in moves):
                    raise SolverError('Solver returned an unrecognized move.')
                self.result = moves
                self.close()
        except Exception as error:
            self.error = str(error)
            self.close()

    def cancel(self):
        if not self.done:
            self.error = 'Solve cancelled.'
        self.close()

    def close(self):
        if self._closed:
            return
        self._closed = True
        atexit.unregister(self.close)
        if self.process is not None and self.process.poll() is None:
            self.process.kill()
            self.process.wait()
        for stream in (self._output, self._errors):
            if stream is not None:
                stream.close()
        self._temp.cleanup()
