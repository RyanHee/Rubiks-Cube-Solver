from Rubiks_Cube import Cube
from Rubiks_Cube import CubeVisualizer


'''
test_cube_lst = [
    [['W' for _ in range(3)] for _ in range(3)],
    [['O' for _ in range(3)] for _ in range(3)],
    [['G' for _ in range(3)] for _ in range(3)],
    [['G', 'G', 'G'], ['W', 'W', 'W'], ['W', 'W', 'W']],
    [['B' for _ in range(3)] for _ in range(3)],
    [['Y' for _ in range(3)] for _ in range(3)]
]
'''

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


initial_cube = Cube()
initial_cube.R()
cube_visualizer = CubeVisualizer(initial_cube.cube)

cube_visualizer.app.input = cube_visualizer.input
cube_visualizer.app.update = cube_visualizer.update

cube_visualizer.run()