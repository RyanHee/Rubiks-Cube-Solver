import numpy as np
from ursina import *
from ursina.shaders import unlit_shader


class Cube:
    def __init__(self, cube_list=None):
        if cube_list is not None:
            temp_cube = np.array(cube_list)
            if isinstance(temp_cube, np.ndarray) and temp_cube.shape == (6, 3, 3):
                self.cube = temp_cube
                return
        lst = ['W', 'O', 'G', 'R', 'B', 'Y']
        temp = list()
        for it in lst:
            face = [[it for _ in range(3)] for _ in range(3)]
            temp.append(face)
        self.cube = np.array(temp)

    def reset(self):
        lst = ['W', 'O', 'G', 'R', 'B', 'Y']
        temp = list()
        for it in lst:
            face = [[it for _ in range(3)] for _ in range(3)]
            temp.append(face)
        self.cube = np.array(temp)

    def move(self, turn):
        if len(turn) == 2:
            if turn[1] == '2':
                if turn[0] == 'R':
                    self.R(2)
                elif turn[0] == 'U':
                    self.U(2)
                elif turn[0] == 'L':
                    self.L(2)
                elif turn[0] == 'D':
                    self.D(2)
                elif turn[0] == 'F':
                    self.F(2)
                elif turn[0] == 'B':
                    self.B(2)
            elif turn[1] == '\'':
                if turn[0] == 'R':
                    self.RPrime()
                elif turn[0] == 'U':
                    self.UPrime()
                elif turn[0] == 'L':
                    self.LPrime()
                elif turn[0] == 'D':
                    self.DPrime()
                elif turn[0] == 'F':
                    self.FPrime()
                elif turn[0] == 'B':
                    self.BPrime()
        else:
            if turn == 'R':
                self.R()
            elif turn == 'U':
                self.U()
            elif turn == 'L':
                self.L()
            elif turn == 'D':
                self.D()
            elif turn == 'F':
                self.F()
            elif turn == 'B':
                self.B()

    def R(self, k=1):
        for _ in range(k):
            # shift right side up
            faces = [0, 2, 5, 4]
            lst = []
            for it in faces:
                temp = []
                if it == 4:
                    for i in range(3):
                        temp.append(self.cube[it, i, 0])
                    temp.reverse()
                else:
                    for i in range(3):
                        temp.append(self.cube[it, i, 2])
                lst.append(temp)
            lst.append(lst.pop(0))
            lst.reverse()
            for it in faces:
                temp = lst.pop()
                if it == 4:
                    for i in range(3):
                        self.cube[it, i, 0] = temp[i]
                else:
                    for i in range(3):
                        self.cube[it, i, 2] = temp[i]
            # rotate right side (red)
            self.cube[3] = np.rot90(self.cube[3], k=3)
        #print(self.cube)

    def RPrime(self, k=1):
        for _ in range(k):
            # shift right side down
            faces = [0, 2, 5, 4]
            lst = []
            for it in faces:
                temp = []
                if it == 4:
                    for i in range(3):
                        temp.append(self.cube[it, i, 0])
                    temp.reverse()
                else:
                    for i in range(3):
                        temp.append(self.cube[it, i, 2])
                lst.append(temp)
            lst.insert(0, lst.pop())
            lst.reverse()
            for it in faces:
                temp = lst.pop()
                #print(temp)
                if it == 4:
                    for i in range(3):
                        self.cube[it, i, 0] = temp[i]
                else:
                    for i in range(3):
                        self.cube[it, i, 2] = temp[i]
            # rotate right side (red)
            self.cube[3] = np.rot90(self.cube[3])
        #print(self.cube)

    def L(self, k=1):
        for _ in range(k):
            # shift left side down
            faces = [0, 2, 5, 4]
            lst = []
            for it in faces:
                temp = []
                if it == 4:
                    for i in range(3):
                        temp.append(self.cube[it, i, 2])
                    temp.reverse()
                else:
                    for i in range(3):
                        temp.append(self.cube[it, i, 0])
                lst.append(temp)
            lst.insert(0, lst.pop())
            lst.reverse()
            for it in faces:
                temp = lst.pop()
                if it == 4:
                    for i in range(3):
                        self.cube[it, i, 2] = temp[i]
                else:
                    for i in range(3):
                        self.cube[it, i, 0] = temp[i]
            # rotate left side (orange)
            self.cube[1] = np.rot90(self.cube[1], k=3)
        #print(self.cube)

    def LPrime(self, k=1):
        for _ in range(k):
            # shift left side up
            faces = [0, 2, 5, 4]
            lst = []
            for it in faces:
                temp = []
                if it == 4:
                    for i in range(3):
                        temp.append(self.cube[it, i, 2])
                    temp.reverse()
                else:
                    for i in range(3):
                        temp.append(self.cube[it, i, 0])
                lst.append(temp)
            lst.append(lst.pop(0))
            lst.reverse()
            for it in faces:
                temp = lst.pop()
                if it == 4:
                    for i in range(3):
                        self.cube[it, i, 2] = temp[i]
                else:
                    for i in range(3):
                        self.cube[it, i, 0] = temp[i]
            # rotate left side (orange)
            self.cube[1] = np.rot90(self.cube[1])
        #print(self.cube)

    def U(self, k=1):
        for _ in range(k):
            # shift top side to the left <-
            faces = [1, 2, 3, 4]
            lst = []
            for it in faces:
                temp = self.cube[it, 0].copy()
                lst.append(temp)
            lst.append(lst.pop(0))
            lst.reverse()
            for it in faces:
                self.cube[it, 0] = lst.pop()
            # rotate top side (white)
            self.cube[0] = np.rot90(self.cube[0], k=3)
        #print(self.cube)

    def UPrime(self, k=1):
        for _ in range(k):
            # shift top side to the right ->
            faces = [1, 2, 3, 4]
            lst = []
            for it in faces:
                temp = self.cube[it, 0].copy()
                lst.append(temp)
            lst.insert(0, lst.pop())
            lst.reverse()
            for it in faces:
                self.cube[it, 0] = lst.pop()
            # rotate top side (white)
            self.cube[0] = np.rot90(self.cube[0])
        #print(self.cube)

    def B(self, k=1):
        for _ in range(k):
            # shift back to right left <-
            lst = [self.cube[0, 0].copy(), [self.cube[3, 0, 2], self.cube[3, 1, 2], self.cube[3, 2, 2]],
                   self.cube[5, 2].copy(), [self.cube[1, 0, 0], self.cube[1, 1, 0], self.cube[1, 2, 0]]]
            lst.append(lst.pop(0))
            lst.reverse()
            self.cube[0, 0] = lst.pop()
            temp = lst.pop()
            for i in range(3):
                self.cube[3, i, 2] = temp[i]
            self.cube[5, 2] = lst.pop()
            temp = lst.pop()
            for i in range(3):
                self.cube[1, i, 0] = temp[i]
            # rotate back side (blue)
            self.cube[4] = np.rot90(self.cube[4], k=3)
        #print(self.cube)

    def BPrime(self, k=1):
        for _ in range(k):
            # shift back side to the right ->
            lst = [self.cube[0, 0].copy(), [self.cube[3, 0, 2], self.cube[3, 1, 2], self.cube[3, 2, 2]],
                   self.cube[5, 2].copy(), [self.cube[1, 0, 0], self.cube[1, 1, 0], self.cube[1, 2, 0]]]
            lst.insert(0, lst.pop())
            lst.reverse()
            self.cube[0, 0] = lst.pop()
            temp = lst.pop()
            for i in range(3):
                self.cube[3, i, 2] = temp[i]
            self.cube[5, 2] = lst.pop()
            temp = lst.pop()
            for i in range(3):
                self.cube[1, i, 0] = temp[i]
            # rotate back side (blue)
            self.cube[4] = np.rot90(self.cube[4])
        #print(self.cube)

    def F(self, k=1):
        for _ in range(k):
            # shift front to right ->
            lst = [self.cube[0, 2].copy(), [self.cube[3, 0, 0], self.cube[3, 1, 0], self.cube[3, 2, 0]],
                   self.cube[5, 0].copy(), [self.cube[1, 0, 2], self.cube[1, 1, 2], self.cube[1, 2, 2]]]
            lst.insert(0, lst.pop())
            lst.reverse()
            self.cube[0, 2] = lst.pop()
            temp = lst.pop()
            for i in range(3):
                self.cube[3, i, 0] = temp[i]
            self.cube[5, 0] = lst.pop()
            temp = lst.pop()
            for i in range(3):
                self.cube[1, i, 2] = temp[i]
            # rotate front side (green)
            self.cube[2] = np.rot90(self.cube[2], k=3)
        #print(self.cube)

    def FPrime(self, k=1):
        for _ in range(k):
            # shift front to left <-
            lst = [self.cube[0, 2].copy(), [self.cube[3, 0, 0], self.cube[3, 1, 0], self.cube[3, 2, 0]],
                   self.cube[5, 0].copy(), [self.cube[1, 0, 2], self.cube[1, 1, 2], self.cube[1, 2, 2]]]
            lst.append(lst.pop(0))
            lst.reverse()
            self.cube[0, 2] = lst.pop()
            temp = lst.pop()
            for i in range(3):
                self.cube[3, i, 0] = temp[i]
            self.cube[5, 0] = lst.pop()
            temp = lst.pop()
            for i in range(3):
                self.cube[1, i, 2] = temp[i]
            # rotate front side (green)
            self.cube[2] = np.rot90(self.cube[2])
        #print(self.cube)

    def D(self, k=1):
        for _ in range(k):
            # shift bottom side to the right ->
            faces = [1, 2, 3, 4]
            lst = []
            for it in faces:
                temp = self.cube[it, 2].copy()
                lst.append(temp)
            lst.insert(0, lst.pop())
            lst.reverse()
            for it in faces:
                self.cube[it, 2] = lst.pop()
            # rotate bottom side (yellow)
            self.cube[5] = np.rot90(self.cube[5], k=3)
        #print(self.cube)

    def DPrime(self, k=1):
        for _ in range(k):
            # shift bottom side to the left <-
            faces = [1, 2, 3, 4]
            lst = []
            for it in faces:
                temp = self.cube[it, 2].copy()
                lst.append(temp)
            lst.append(lst.pop(0))
            lst.reverse()
            for it in faces:
                self.cube[it, 2] = lst.pop()
            # rotate bottom side (yellow)
            self.cube[5] = np.rot90(self.cube[5])
        #print(self.cube)


class Cubelet:
    def __init__(self):
        self.colors = [""] * 6


class CubeVisualizer:
    def __init__(self, cube):
        self.init_maps()
        self.cube = cube
        self.cube_array = np.array(cube.cube)
        self.core = Entity()
        self.cubelets = [[[Cubelet() for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.turn_duration = 1
        self.can_action=True
        self.app = Ursina()
        self.cube_entity = Entity()
        self.mouse_start = None
        self.cube_entity.shader = unlit_shader

        self._assign_colors()
        self.build_cube()
        print(self.cubelet_entities)
        EditorCamera()
        DirectionalLight(parent=scene, direction=(1, -1, -1), color=color.white)
        Sky()

        def global_input(key):
            self.input(key)

        def global_update():
            self.update()

        window.input = global_input
        window.update = global_update

    def init_maps(self):
        self.cubelet_entities = {}

        # x y z
        self.cube_to_rot = {
            'R': [(1, y, z) for y in range(-1,2) for z in range(-1,2)],
            'L': [(-1, y, z) for y in range(-1,2) for z in range(-1,2)],
            'U': [(x, 1, z) for x in range(-1,2) for z in range(-1,2)],
            'D': [(x, -1, z) for x in range(-1,2) for z in range(-1,2)],
            'F': [(x, y, 1) for x in range(-1,2) for y in range(-1,2)],
            'B': [(x, y, -1) for x in range(-1,2) for y in range(-1,2)],
        }

        self.rot_axis = {
            'R': 'x',
            'L': 'x',
            'U': 'y',
            'D': 'y',
            'F': 'z',
            'B': 'z',
        }

        self.rot_angle = {
            '': '90',
            '\'': '-90',
            '2': '180'
        }

        self.color_map = {
            'W': color.white,
            'O': color.orange,
            'G': color.green,
            'R': color.red,
            'B': color.blue,
            'Y': color.yellow
        }

    def create_solved_array(self):
        lst = ['W', 'O', 'G', 'R', 'B', 'Y']
        temp = []
        for c in lst:
            face = [[c for _ in range(3)] for _ in range(3)]
            temp.append(face)
        return temp

    def _assign_colors(self):

        #print(self.cube_array[0])
        for row in range(3):
            for col in range(3):
                color_char = self.cube_array[0, row, col]
                x = col - 1
                y = 1
                z = 1 - row
                self._set_cubelet_face(x, y, z, 0, color_char)

        for row in range(3):
            for col in range(3):
                color_char = self.cube_array[5, row, col]
                x = col - 1
                y = -1
                z = row - 1
                self._set_cubelet_face(x, y, z, 5, color_char)

        for row in range(3):
            for col in range(3):
                color_char = self.cube_array[2, row, col]
                #print(color_char)

                x = col - 1
                y = 1 - row
                z = -1
                self._set_cubelet_face(x, y, z, 4, color_char)

        for row in range(3):
            for col in range(3):
                color_char = self.cube_array[4, row, col]
                x = 1 - col
                y = 1 - row
                z = 1
                self._set_cubelet_face(x, y, z, 2, color_char)

        for row in range(3):
            for col in range(3):
                color_char = self.cube_array[1, row, col]
                x = -1
                y = 1 - row
                z = 1 - col
                self._set_cubelet_face(x, y, z, 1, color_char)

        for row in range(3):
            for col in range(3):
                color_char = self.cube_array[3, row, col]
                x = 1
                y = 1 - row
                z = col - 1
                self._set_cubelet_face(x, y, z, 3, color_char)

    def _set_cubelet_face(self, x, y, z, face_index, color_char):
        xi = x + 1
        yi = y + 1
        zi = z + 1
        self.cubelets[zi][yi][xi].colors[face_index] = color_char

    def build_cube(self):
        # Create entities for cubelets
        for zi in range(3):
            for yi in range(3):
                for xi in range(3):
                    cubelet = self.cubelets[zi][yi][xi]
                    x = xi - 1
                    y = yi - 1
                    z = zi - 1

                    cubelet_entity = Entity(parent=self.cube_entity,
                                            position=(x, y, z),
                                            model='cube',
                                            scale=1,
                                            color=color.black,
                                            visible=True)
                    self.cubelet_entities[(x, y, z)] = cubelet_entity
                    self.add_stickers(cubelet_entity, cubelet)

    def add_stickers(self, parent_entity, cubelet):
        # Face directions:
        directions = {
            0: ((0, 0.55, 0), (90, 0, 0)),  # Up (White)
            5: ((0, -0.55, 0), (-90, 0, 0)),  # Down (Yellow)
            2: ((0, 0, 0.55), (0, 180, 0)),  # Front (Green)
            4: ((0, 0, -0.55), (0, 0, 0)),  # Back (Blue)
            1: ((-0.55, 0, 0), (0, 90, 0)),  # Left (Orange)
            3: ((0.55, 0, 0), (0, -90, 0))  # Right (Red)
        }

        for face_index, face_color_char in enumerate(cubelet.colors):
            if face_color_char in self.color_map and face_color_char != "":
                local_pos, local_rot = directions[face_index]
                Entity(parent=parent_entity,
                       model='quad',
                       scale=0.9,
                       position=local_pos,
                       rotation=local_rot,
                       color=self.color_map[face_color_char])

    def input(self, key):
        print(key)
        if not self.can_action:
            return
        if key == 'left mouse down':
            self.mouse_start = mouse.position
        elif key == 'left mouse up':
            self.mouse_start = None
        elif key in 'ruldfb':
            self.rotate(key.upper())

    def reparent(self):
        for xi in range(-1,2):
            for yi in range(-1,2):
                for zi in range(-1,2):
                    cubelet_entity = self.cubelet_entities[(xi, yi, zi)]
                    if cubelet_entity.parent == self.core:
                        world_pos, world_rot = round(cubelet_entity.world_position, 1), cubelet_entity.world_rotation
                        cubelet_entity.position, cubelet_entity.rotation = world_pos, world_rot
                        cubelet_entity.parent = self.cube_entity
        self.core.rotation = 0

    def rotate(self, move):
        print(move)
        self.can_action=False
        #self.reparent()
        rotate_axis = self.rot_axis[move[0]]
        temp_s = ''
        if len(move) != 1:
            temp_s = move[1]
        rotate_angle = self.rot_angle[temp_s]
        for xi, yi, zi in self.cube_to_rot[move]:
            cubelet_entity = self.cubelet_entities[(xi, yi, zi)]
            cubelet_entity.parent = self.core

            eval(f'self.core.animate_rotation_{rotate_axis}({rotate_angle}, duration = self.turn_duration)')
        invoke(self.reparent, delay=self.turn_duration+0.05)
        invoke(self.trigger_action, delay=self.turn_duration+0.05)


    def trigger_action(self):
        self.can_action=True

    def update(self):
        if mouse.left and self.mouse_start is not None:
            drag = mouse.position - self.mouse_start
            self.cube_entity.rotation_y += drag.x * 100
            self.cube_entity.rotation_x -= drag.y * 100
            self.mouse_start = mouse.position

    def run(self):
        self.app.run()
