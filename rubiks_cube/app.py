"""Load the initial cube state and start its visualizer."""

from pathlib import Path

from .cube import Cube, CubeVisualizer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
cube_visualizer = None


def input(key):
    """Ursina calls this through the launcher's __main__ module."""
    if cube_visualizer is not None:
        cube_visualizer.input(key)


def main():
    global cube_visualizer
    state_path = PROJECT_ROOT / 'data/cube_init.txt'
    facelets = [
        [list(row) for row in line.split()]
        for line in state_path.read_text().splitlines()
    ]
    cube = Cube(facelets)
    cube_visualizer = CubeVisualizer(cube)
    cube_visualizer.run()
