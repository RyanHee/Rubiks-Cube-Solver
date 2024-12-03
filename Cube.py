import numpy as np


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
                if it==4:
                    for i in range(3):
                        temp.append(self.cube[it, i, 0])
                else:
                    for i in range(3):
                        temp.append(self.cube[it, i, 2])
                lst.append(temp)
            lst.append(lst.pop(0))
            lst.reverse()
            for it in faces:
                temp = lst.pop()
                if it==4:

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
                for i in range(3):
                    temp.append(self.cube[it, i, 2])
                lst.append(temp)
            lst.insert(0, lst.pop())
            lst.reverse()
            for it in faces:
                temp = lst.pop()
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
                for i in range(3):
                    temp.append(self.cube[it, i, 0])
                lst.append(temp)
            lst.insert(0, lst.pop())
            lst.reverse()
            for it in faces:
                temp = lst.pop()
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
                for i in range(3):
                    temp.append(self.cube[it, i, 0])
                lst.append(temp)
            lst.append(lst.pop(0))
            lst.reverse()
            for it in faces:
                temp = lst.pop()
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
            temp=lst.pop()
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
            temp=lst.pop()
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
            temp=lst.pop()
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
            temp=lst.pop()
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