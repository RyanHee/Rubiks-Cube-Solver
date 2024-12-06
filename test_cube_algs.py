import unittest
import numpy as np
from Rubiks_Cube import Cube


class MyTestCase(unittest.TestCase):
    def test_moves(self):
        test_cube_lst = []
        with open('cube_init.txt', 'r') as f:
            for line in f:
                lst = line.strip().split(' ')
                for i in range(3):
                    lst[i] = [it for it in lst[i]]
                test_cube_lst.append(lst)
        c = Cube(test_cube_lst)
        algs = []
        with open('cube_algs.txt', 'r') as f:
            for line in f:
                algs.append(line.strip())

        ans = []
        with open('cube_ans.txt', 'r') as f:
            for i in range(1):
                cube_lst = []
                for k in range(6):
                    lst = f.readline().strip().split(' ')
                    for j in range(3):
                        lst[j] = [it for it in lst[j]]
                    cube_lst.append(lst)
                #print(cube_lst)
                np_cube_lst = np.array(cube_lst)
                ans.append(np_cube_lst)
        print(len(ans))
        for i in range(len(ans)):
            c.reset()
            for move in algs[i].split():
                c.move(move)
            print(i)
            print(algs[i])
            print(c.cube)
            np.testing.assert_array_equal(c.cube, ans[i])
            #self.assertEqual(ans[i].all(), c.cube.all())

        #self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
