"""Mode selection and sticker entry UI. Palette colors never change piece IDs."""
from collections import Counter
from functools import partial
from math import cos, sin, pi
import sys

from panda3d.core import TransparencyAttrib

from ursina import Entity, Button, Text, Mesh, Vec3, camera, color, destroy, window
from ursina.shaders import unlit_shader

from .cube import Cube
from .cube_state import FACE_COLORS
from .solver import SolverJob

# W, O, G, R, B, Y. Labels keep the editor usable with stylized palettes.
PALETTES = (
    ('Classic', ('F4F4F0', 'FF8A24', '24B86A', 'E84B55', '4088ED', 'F6D64A')),
    ('Bright', ('FFFFFF', 'FF9E00', '00DB72', 'FF354A', '2675FF', 'FFE500')),
    ('Pastel', ('F8F2EB', 'F6BB89', '99D7B0', 'F2A1AD', 'A4C8F0', 'F5E69B')),
    ('Muted', ('E3DDD2', 'C58B57', '709C84', 'BA7376', '748FAE', 'CDBD75')),
    ('Ocean', ('EAF6FA', 'EFAC76', '57C7AC', 'E7788D', '428DBB', 'E9DA8B')),
    ('Neon', ('F3F3FF', 'FF962E', '71F542', 'FF3F8C', '5A7DFF', 'F5F54A')),
    ('Earth', ('EEE5D5', 'C77940', '718B4D', 'AF5549', '638597', 'D7B859')),
    ('Candy', ('FFF1F5', 'FFB16D', '7EDDB6', 'F16E9E', '9B98EA', 'F5E287')),
    ('Jewel', ('EDE9E1', 'D58A3D', '208E72', 'C43C62', '4961BA', 'D9BC42')),
    ('High contrast', ('FFFFFF', 'FF9200', '00A66A', 'CC244B', '2455D6', 'FFE04A')),
)
FACE_NAMES = ('U / White', 'L / Orange', 'F / Green', 'R / Red', 'B / Blue', 'D / Yellow')


def rgb(value):
    return color.rgb32(*[int(value[i:i + 2], 16) for i in (0, 2, 4)])


class CubeGUI:
    def __init__(self, visualizer):
        self.view = visualizer
        self.mode = None
        self.palette_index = 0
        self.selected = 'W'
        self.stickers = Cube().cube.copy()
        self.validated_state = None
        self.root = None
        self.job = None
        self.playing = False
        self.solution = ()
        self.step_index = 0
        self.playback_speed = 1.0
        self.move_arrow = None
        self.arrow_move = None
        self.driver = Entity()
        self.driver.update = self.update
        window.title = 'Cube Studio'
        window.editor_ui.enabled = False
        self.show_home()

    @property
    def palette(self):
        return dict(zip(FACE_COLORS, map(rgb, PALETTES[self.palette_index][1])))

    def clear(self, mode):
        if self.move_arrow is not None:
            destroy(self.move_arrow)
            self.move_arrow = None
        self.arrow_move = None
        if self.job is not None:
            self.job.cancel()
            self.job = None
        self.playing = False
        if self.root is not None:
            destroy(self.root)
        self.mode = mode
        self.root = Entity(parent=camera.ui)
        is_3d = mode in ('simulator', 'solution')
        self.view.cube_entity.enabled = is_3d
        self.view.core.enabled = is_3d
        self.view.editor_camera.enabled = is_3d
        self.view.editor_camera.ignore_input = not is_3d
        if not is_3d:
            Entity(parent=self.root, model='quad', scale=(4, 2), z=.5,
                   color=color.rgb32(19, 24, 35))

    def text(self, text, x, y, scale=1, **kwargs):
        entity = Text(parent=self.root, text=text, x=x, y=y, scale=scale, **kwargs)
        self.fix_transparency()
        return entity

    def fix_transparency(self):
        if sys.platform == 'darwin':
            for node in camera.ui_render.findAllMatches('**'):
                if node.getTransparency() == TransparencyAttrib.M_dual:
                    node.setTransparency(TransparencyAttrib.M_alpha)

    def button(self, text, x, y, action, width=.23, height=.045, **kwargs):
        entity = Button(parent=self.root, text=text, x=x, y=y,
                      scale=(width, height), on_click=action,
                      color=color.rgb32(45, 58, 79), **kwargs)
        self.fix_transparency()
        return entity

    def show_home(self):
        if not self.view.can_action:
            return
        self.clear('home')
        self.text('CUBE STUDIO', -.60, .32, 2.5)
        self.text('Explore the cube. Find your next move.', -.60, .23, 1.05)
        self.button('SIMULATOR', -.32, .04, self.show_simulator, .48, .14)
        self.button('SOLVER / STICKER INPUT', .27, .04, self.show_editor, .48, .14)
        self.text('Turn, orbit, and experiment.', -.55, -.08, .85)
        self.text('Enter your cube and check its state.', .04, -.08, .85)
        self.text('Choose a mode to begin. You can return here at any time.', -.60, -.28, .9,
                  color=color.rgb32(165, 178, 199))

    def show_simulator(self):
        self.clear('simulator')
        self.text('SIMULATOR', -.76, .45, 1.25)
        self.button('Modes', .67, .44, self.show_home, .16)
        self.text('R U L D F B: turn    T I ; S G N: prime\nRight-drag: orbit    Scroll: zoom',
                  -.76, -.39, .8)

    def show_editor(self):
        self.clear('editor')
        self.text('ENTER YOUR CUBE', -.77, .46, 1.7)
        self.button('Modes', .67, .44, self.show_home, .16)
        self.text('Pick a color, then click stickers. Centers stay fixed.', -.77, .39, .87)
        self.text('Faces are viewed from outside. Keep white up and green in front.',
                  -.77, .345, .76, color=color.rgb32(170, 184, 205))
        self.cells = {}
        # Unfolded net: U above F; L F R B across; D below F.
        for face, (cx, cy) in enumerate(((-.34, .205), (-.55, -.015),
                                       (-.34, -.015), (-.13, -.015),
                                       (.08, -.015), (-.34, -.235))):
            self.text(FACE_NAMES[face], cx - .085, cy + .123, .67)
            for row in range(3):
                for col in range(3):
                    button = self.button(FACE_COLORS[face] if row == col == 1 else '',
                                         cx + (col - 1) * .058, cy + (1 - row) * .058,
                                         partial(self.paint, face, row, col), .054, .054)
                    if button.text_entity is not None:
                        button.text_entity.color = color.black
                    self.cells[face, row, col] = button
        self.text('PAINT COLOR', .31, .29, .85)
        self.brushes = {}
        for index, name in enumerate(FACE_COLORS):
            button = self.button(name, .35 + index % 3 * .105,
                                 .22 - index // 3 * .075,
                                 partial(self.select, name), .088, .058)
            button.text_entity.color = color.black
            self.brushes[name] = button
        self.selection_text = self.text('', .31, .09, .8)
        self.text('PALETTE', .31, .025, .85)
        self.palette_text = self.text('', .35, -.025, .85)
        self.button('Prev', .31, -.075, partial(self.change_palette, -1), .07)
        self.button('Next', .58, -.075, partial(self.change_palette, 1), .07)
        self.button('Reset to solved', .445, -.15, self.reset_editor, .29)
        self.button('Validate cube', .445, -.215, self.validate, .29, .055)
        self.preview_button = self.button('Open in simulator', .445, -.285, self.preview, .29)
        self.preview_button.enabled = self.validated_state is not None
        self.solve_button = self.button('Solve cube', .445, -.35, self.start_solve, .29, .055)
        self.status = self.text('Enter stickers, then validate your cube.',
                                -.77, -.405, .8, wordwrap=85)
        self.refresh()

    def select(self, name):
        self.selected = name
        self.refresh()

    def paint(self, face, row, col):
        if row == col == 1:
            return
        self.cancel_solve()
        self.stickers[face, row, col] = self.selected
        self.validated_state = None
        self.preview_button.enabled = False
        self.status.text = 'Stickers changed. Validate when ready.'
        self.status.color = color.white
        self.refresh()

    def refresh(self):
        palette = self.palette
        for index, button in self.cells.items():
            button.color = palette[self.stickers[index]]
            button.highlight_color = button.color.tint(.15)
            button.pressed_color = button.color.tint(-.15)
        counts = Counter(self.stickers.ravel())
        for name, button in self.brushes.items():
            button.color = palette[name]
            button.highlight_color = button.color.tint(.15)
            button.text = f'{name} {counts[name]}/9'
            button.text_entity.color = color.black
            button.text_size = .7
        self.selection_text.text = f'Painting: {self.selected}'
        self.palette_text.text = f'{self.palette_index + 1}/10  {PALETTES[self.palette_index][0]}'

    def change_palette(self, direction):
        self.palette_index = (self.palette_index + direction) % len(PALETTES)
        self.refresh()

    def reset_editor(self):
        self.cancel_solve()
        self.stickers = Cube().cube.copy()
        self.validated_state = None
        self.preview_button.enabled = False
        self.status.text = 'Reset to solved. Click stickers to enter your cube.'
        self.status.color = color.white
        self.refresh()

    def validate(self):
        try:
            state = Cube(self.stickers).to_cubestate()
        except ValueError as error:
            self.validated_state = None
            self.preview_button.enabled = False
            self.status.text = f'Check your stickers: {error}'
            self.status.color = color.rgb32(255, 157, 157)
            return
        self.validated_state = state
        self.status.text = 'Valid cube. Ready to preview in 3D.'
        self.status.color = color.rgb32(116, 226, 173)
        self.preview_button.enabled = True

    def preview(self):
        self.cancel_solve()
        if self.validated_state is None:
            self.validate()
            return
        self.view.set_cube(Cube(self.stickers), self.palette)
        self.show_simulator()

    def cancel_solve(self):
        if self.job is not None:
            self.job.cancel()
            self.job = None
        if self.mode == 'editor' and hasattr(self, 'solve_button'):
            self.solve_button.text = 'Solve cube'

    def start_solve(self):
        if self.job is not None:
            self.cancel_solve()
            self.status.text = 'Solve cancelled. You can try again.'
            return
        self.validate()
        if self.validated_state is None:
            return
        self.solve_stickers = self.stickers.copy()
        self.job = SolverJob(self.validated_state)
        self.solve_button.text = 'Cancel solve'
        self.status.text = self.job.stage + '...'

    def show_solution(self, moves):
        self.solution = moves
        self.step_index = 0
        self.view.set_cube(Cube(self.solve_stickers), self.palette)
        self.clear('solution')
        self.text('YOUR SOLUTION', -.73, .45, 1.3)
        self.text('Arrow direction is viewed from outside the turning face.', -.73, .40, .75)
        self.button('Modes', .67, .44, self.show_home, .16)
        Entity(parent=self.root, model='quad', scale=(4, .24), y=-.39, z=.2,
               color=color.rgb32(19, 24, 35))
        self.progress = self.text('', -.73, -.285, .9)
        self.algorithm = self.text(' '.join(moves) if moves else 'Your cube is already solved.',
                                   -.73, -.33, .77, wordwrap=105)
        self.play_button = self.button('Play', -.61, -.435, self.toggle_play, .20)
        self.next_button = self.button('Next move', -.36, -.435, self.next_move, .22)
        self.restart_button = self.button('Restart', -.10, -.435, self.restart_solution, .22)
        self.edit_button = self.button('Edit stickers', .18, -.435, self.edit_solution, .26)
        self.button('-', .39, -.435, partial(self.change_speed, -1), .065)
        self.speed_label = self.text('', .44, -.42, .85)
        self.button('+', .70, -.435, partial(self.change_speed, 1), .065)
        self.text('Playback speed', .39, -.385, .66)
        self.change_speed(0)
        self.update_progress()

    def change_speed(self, direction):
        speeds = (.25, .5, .75, 1., 1.5, 2., 3., 4.)
        index = speeds.index(self.playback_speed)
        self.playback_speed = speeds[max(0, min(len(speeds) - 1, index + direction))]
        self.speed_label.text = f'{self.playback_speed:g}x'

    def show_move_arrow(self, move):
        """Draw a curved arrow just outside the face, in its local sticker plane."""
        if move == self.arrow_move:
            return
        self.arrow_move = move
        if self.move_arrow is not None:
            destroy(self.move_arrow)
            self.move_arrow = None
        if move is None:
            return
        normal, right, up = {
            'F': ((0, 0, -1), (1, 0, 0), (0, 1, 0)),
            'B': ((0, 0, 1), (-1, 0, 0), (0, 1, 0)),
            'R': ((1, 0, 0), (0, 0, 1), (0, 1, 0)),
            'L': ((-1, 0, 0), (0, 0, -1), (0, 1, 0)),
            'U': ((0, 1, 0), (1, 0, 0), (0, 0, 1)),
            'D': ((0, -1, 0), (1, 0, 0), (0, 0, -1)),
        }[move[0]]
        normal, right, up = Vec3(*normal), Vec3(*right), Vec3(*up)
        center = normal * 1.65
        direction = 1 if move.endswith("'") else -1
        sweep = pi if move.endswith('2') else pi / 2
        angles = [pi * .75 + direction * sweep * i / 40 for i in range(41)]
        points = [center + (right * cos(a) + up * sin(a)) * 1.9 for a in angles]
        # A triangle ribbon remains visible on all graphics backends.
        vertices, triangles = [], []
        for a, point in zip(angles, points):
            radial = right * cos(a) + up * sin(a)
            vertices.extend((point - radial * .045, point + radial * .045))
        for i in range(40):
            j = i * 2
            triangles.extend(((j, j + 1, j + 2), (j + 1, j + 3, j + 2)))
        tangent = (right * -sin(angles[-1]) + up * cos(angles[-1])) * direction
        radial = right * cos(angles[-1]) + up * sin(angles[-1])
        base = len(vertices)
        vertices.extend((points[-1] + tangent * .28,
                         points[-1] - tangent * .12 + radial * .18,
                         points[-1] - tangent * .12 - radial * .18))
        triangles.append((base, base + 1, base + 2))
        self.move_arrow = Entity(model=Mesh(vertices=vertices, triangles=triangles),
                                 color=color.rgb32(255, 213, 71), shader=unlit_shader,
                                 double_sided=True)

    def update_progress(self):
        finished = self.step_index == len(self.solution) and self.view.can_action
        if finished:
            self.playing = False
        next_move = self.solution[self.step_index] if self.step_index < len(self.solution) else 'done'
        turning = not self.view.can_action and self.step_index > 0
        indicated_move = self.solution[self.step_index - 1] if turning else (None if finished else next_move)
        self.show_move_arrow(indicated_move)
        direction = ('180 degrees' if indicated_move and indicated_move.endswith('2') else
                     'counterclockwise' if indicated_move and indicated_move.endswith("'") else 'clockwise')
        progress = ('Solved!' if finished else
                    f'Move {self.step_index}/{len(self.solution)}    {"Turning" if turning else "Next"}: {indicated_move} ({direction})')
        if self.progress.text != progress:
            self.progress.text = progress
        label = 'Pause' if self.playing else 'Play'
        if self.play_button.text != label:
            self.play_button.text = label
        self.play_button.disabled = finished
        self.next_button.disabled = self.playing or not self.view.can_action or finished
        self.restart_button.disabled = not self.view.can_action
        self.edit_button.disabled = not self.view.can_action

    def toggle_play(self):
        self.playing = not self.playing
        self.update_progress()

    def next_move(self):
        if self.view.can_action and self.step_index < len(self.solution):
            self.view.rotate(self.solution[self.step_index], duration=.5 / self.playback_speed)
            self.step_index += 1
            self.update_progress()

    def restart_solution(self):
        if not self.view.can_action:
            return
        self.playing = False
        self.step_index = 0
        self.view.set_cube(Cube(self.solve_stickers), self.palette)
        self.update_progress()

    def edit_solution(self):
        if self.view.can_action:
            self.show_editor()

    def update(self):
        if self.job is not None:
            self.job.poll()
            status = self.job.stage + '...'
            if self.status.text != status:
                self.status.text = status
            if self.job.done:
                job, self.job = self.job, None
                self.solve_button.text = 'Solve cube'
                if job.error:
                    self.status.text = job.error
                    self.status.color = color.rgb32(255, 157, 157)
                else:
                    # Independently check the returned path against Python stickers.
                    check = Cube(self.solve_stickers)
                    for move in job.result:
                        check.move(move)
                    if check.to_cubestate() != Cube().to_cubestate():
                        self.status.text = 'The returned moves did not solve this cube.'
                        self.status.color = color.rgb32(255, 157, 157)
                    else:
                        self.show_solution(job.result)
        if self.mode == 'solution':
            if self.playing and self.view.can_action:
                self.next_move()
            self.update_progress()

    def input(self, key):
        if self.mode == 'simulator':
            self.view.input(key)
        if key == 'escape':
            self.show_home()
