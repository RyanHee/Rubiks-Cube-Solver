"""Load the initial cube state and start its visualizer."""

from pathlib import Path

from .cube import Cube, CubeVisualizer
from .gui import CubeGUI


PROJECT_ROOT = Path(__file__).resolve().parents[1]
cube_visualizer = None
cube_gui = None


def input(key):
    """Ursina calls this through the launcher's __main__ module."""
    if cube_gui is not None:
        cube_gui.input(key)


def main():
    global cube_visualizer, cube_gui
    state_path = PROJECT_ROOT / 'data/cube_init.txt'
    facelets = [
        [list(row) for row in line.split()]
        for line in state_path.read_text().splitlines()
    ]
    cube = Cube(facelets)
    cube_visualizer = CubeVisualizer(cube)
    cube_gui = CubeGUI(cube_visualizer)
    from ursina import window
    window.input = cube_gui.input
    cube_visualizer.run()
