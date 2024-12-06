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

print(test_cube_lst)
c = Cube(test_cube_lst)
s = 'R U R\' F\' R U R\' U\' R\' F R2 U\' R\' U\''.split()

for m in s:
    print(m)
    c.move(m)
    print(c.cube)

initial_cube = Cube()  # Create the Cube instance
cube_visualizer = CubeVisualizer(initial_cube.cube)
cube_visualizer.run()