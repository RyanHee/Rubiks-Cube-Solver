"""Face-turn regressions with distinct labels on all 54 stickers."""

import unittest

import numpy as np

from Rubiks_Cube import Cube


# Each number identifies the source sticker for that destination position.
# Face order: U, L, F, R, B, D; rows viewed from outside each face.
# These fixed expectations come from independent physical rotations, not Cube.
CLOCKWISE_SOURCES = {
    'R': (
         0,  1, 20,  3,  4, 23,  6,  7, 26,  # U
         9, 10, 11, 12, 13, 14, 15, 16, 17,  # L
        18, 19, 47, 21, 22, 50, 24, 25, 53,  # F
        33, 30, 27, 34, 31, 28, 35, 32, 29,  # R
         8, 37, 38,  5, 40, 41,  2, 43, 44,  # B
        45, 46, 42, 48, 49, 39, 51, 52, 36,  # D
    ),
    'L': (
        44,  1,  2, 41,  4,  5, 38,  7,  8,  # U
        15, 12,  9, 16, 13, 10, 17, 14, 11,  # L
         0, 19, 20,  3, 22, 23,  6, 25, 26,  # F
        27, 28, 29, 30, 31, 32, 33, 34, 35,  # R
        36, 37, 51, 39, 40, 48, 42, 43, 45,  # B
        18, 46, 47, 21, 49, 50, 24, 52, 53,  # D
    ),
    'U': (
         6,  3,  0,  7,  4,  1,  8,  5,  2,  # U
        18, 19, 20, 12, 13, 14, 15, 16, 17,  # L
        27, 28, 29, 21, 22, 23, 24, 25, 26,  # F
        36, 37, 38, 30, 31, 32, 33, 34, 35,  # R
         9, 10, 11, 39, 40, 41, 42, 43, 44,  # B
        45, 46, 47, 48, 49, 50, 51, 52, 53,  # D
    ),
    'D': (
         0,  1,  2,  3,  4,  5,  6,  7,  8,  # U
         9, 10, 11, 12, 13, 14, 42, 43, 44,  # L
        18, 19, 20, 21, 22, 23, 15, 16, 17,  # F
        27, 28, 29, 30, 31, 32, 24, 25, 26,  # R
        36, 37, 38, 39, 40, 41, 33, 34, 35,  # B
        51, 48, 45, 52, 49, 46, 53, 50, 47,  # D
    ),
    'F': (
         0,  1,  2,  3,  4,  5, 17, 14, 11,  # U
         9, 10, 45, 12, 13, 46, 15, 16, 47,  # L
        24, 21, 18, 25, 22, 19, 26, 23, 20,  # F
         6, 28, 29,  7, 31, 32,  8, 34, 35,  # R
        36, 37, 38, 39, 40, 41, 42, 43, 44,  # B
        33, 30, 27, 48, 49, 50, 51, 52, 53,  # D
    ),
    'B': (
        29, 32, 35,  3,  4,  5,  6,  7,  8,  # U
         2, 10, 11,  1, 13, 14,  0, 16, 17,  # L
        18, 19, 20, 21, 22, 23, 24, 25, 26,  # F
        27, 28, 53, 30, 31, 52, 33, 34, 51,  # R
        42, 39, 36, 43, 40, 37, 44, 41, 38,  # B
        45, 46, 47, 48, 49, 50,  9, 12, 15,  # D
    ),
}
LABELS = np.arange(54).reshape(6, 3, 3)


class CubeMovementTests(unittest.TestCase):
    def test_standard_clockwise_prime_and_half_turns(self):
        for face, sources in CLOCKWISE_SOURCES.items():
            for suffix, count in (('', 1), ("'", 3), ('2', 2)):
                with self.subTest(move=face + suffix):
                    expected = LABELS.copy().ravel()
                    for _ in range(count):
                        expected = expected[list(sources)]
                    cube = Cube(LABELS)
                    cube.move(face + suffix)
                    np.testing.assert_array_equal(cube.cube, expected.reshape(6, 3, 3))

    def test_turn_and_prime_cancel_in_both_orders(self):
        for face in CLOCKWISE_SOURCES:
            for sequence in ((face, face + "'"), (face + "'", face)):
                with self.subTest(sequence=sequence):
                    cube = Cube(LABELS)
                    for move in sequence:
                        cube.move(move)
                    np.testing.assert_array_equal(cube.cube, LABELS)

    def test_four_quarter_turns_restore_every_sticker(self):
        for face in CLOCKWISE_SOURCES:
            for suffix in ('', "'"):
                with self.subTest(move=face + suffix):
                    cube = Cube(LABELS)
                    for _ in range(4):
                        cube.move(face + suffix)
                    np.testing.assert_array_equal(cube.cube, LABELS)

    def test_two_half_turns_restore_every_sticker(self):
        for face in CLOCKWISE_SOURCES:
            with self.subTest(face=face):
                cube = Cube(LABELS)
                cube.move(face + '2')
                cube.move(face + '2')
                np.testing.assert_array_equal(cube.cube, LABELS)

    def test_direct_methods_repeat_requested_number_of_turns(self):
        for face in CLOCKWISE_SOURCES:
            for prime, suffix in ((False, ''), (True, "'")):
                for count in (0, 1, 2, 3, 4):
                    with self.subTest(face=face, prime=prime, count=count):
                        cube = Cube(LABELS)
                        getattr(cube, face + ('Prime' if prime else ''))(count)
                        expected = Cube(LABELS)
                        for _ in range(count):
                            expected.move(face + suffix)
                        np.testing.assert_array_equal(cube.cube, expected.cube)

    def test_initialization_copies_input_without_reorienting_faces(self):
        source = LABELS.copy()
        cube = Cube(source)
        np.testing.assert_array_equal(cube.cube, source)
        cube.R()
        np.testing.assert_array_equal(source, LABELS)


if __name__ == '__main__':
    unittest.main()
