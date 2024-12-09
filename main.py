from Rubiks_Cube import Cube
from Rubiks_Cube import CubeVisualizer


def input(key):
    cube_visualizer.input(key)

def update():
    cube_visualizer.update()

#print(test_cube_lst)
test_cube_lst = []
with open('cube_init.txt', 'r') as f:
    for line in f:
        lst = line.strip().split(' ')
        for i in range(3):
            lst[i] = [it for it in lst[i]]
        test_cube_lst.append(lst)

#print(test_cube_lst)
c = Cube(test_cube_lst)


cube_visualizer = CubeVisualizer(c)
cube_visualizer.run()