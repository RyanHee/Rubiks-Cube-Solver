"""Validated sticker-to-cubie bridge using the solver's custom JSON mapping.

Faces are U, L, F, R, B, D, each viewed from outside. Centers are fixed
as W, O, G, R, B, Y, matching the simulator and C++ solver.
"""

from collections import Counter
from dataclasses import dataclass
import json
from numbers import Integral
from pathlib import Path

import numpy as np

FACE_COLORS = ('W', 'O', 'G', 'R', 'B', 'Y')
_DATA = Path(__file__).resolve().parents[1] / 'data'


def _mapping(kind, offsets, modulus):
    mapping = json.loads((_DATA / f'{kind}_mapping.json').read_text())
    pieces = sorted(mapping['Position'], key=mapping['Position'].__getitem__)
    # Order sticker positions by orientation, rather than alphabetically.
    ordered = [sorted(piece, key=lambda c: mapping['Orientation'][c] % modulus)
               for piece in pieces]
    return tuple(tuple((ord(c) - ord('A')) // 4 * 9
                       + offsets[(ord(c) - ord('A')) % 4] for c in piece)
                 for piece in ordered)


CORNER_FACELETS = _mapping('corner', (0, 2, 8, 6), 3)
EDGE_FACELETS = _mapping('edge', (1, 5, 7, 3), 2)


def _parity(permutation):
    return sum(a > b for i, a in enumerate(permutation)
               for b in permutation[i + 1:]) % 2


@dataclass(frozen=True)
class CubeState:
    """Immutable cp/co/ep/eo arrays with exactly the C++ IDs and orientations."""

    cp: tuple[int, ...] = tuple(range(8))
    co: tuple[int, ...] = (0,) * 8
    ep: tuple[int, ...] = tuple(range(12))
    eo: tuple[int, ...] = (0,) * 12

    def __post_init__(self):
        for name, length, limit in (('cp', 8, 8), ('co', 8, 3),
                                    ('ep', 12, 12), ('eo', 12, 2)):
            values = tuple(getattr(self, name))
            if len(values) != length or any(
                    isinstance(v, bool) or not isinstance(v, Integral)
                    or not 0 <= v < limit for v in values):
                raise ValueError(f'{name} must contain {length} integers in 0..{limit - 1}')
            object.__setattr__(self, name, tuple(map(int, values)))
        if len(set(self.cp)) != 8 or len(set(self.ep)) != 12:
            raise ValueError('Cube contains duplicate pieces or missing pieces')
        if sum(self.co) % 3:
            raise ValueError('Corner twists must sum to zero modulo 3')
        if sum(self.eo) % 2:
            raise ValueError('Edge flips must sum to zero modulo 2')
        if _parity(self.cp) != _parity(self.ep):
            raise ValueError('Corner and edge permutation parity must match')

    @classmethod
    def from_cube(cls, cube):
        """Validate and snapshot a simulator Cube without changing its stickers."""
        return cls.from_facelets(cube.cube)

    @classmethod
    def from_facelets(cls, facelets):
        """Reject invalid stickers and unreachable positions before creating state."""
        try:
            stickers = np.asarray(facelets)
        except (TypeError, ValueError) as error:
            raise ValueError('Stickers must have shape (6, 3, 3)') from error
        if stickers.shape != (6, 3, 3):
            raise ValueError('Stickers must have shape (6, 3, 3)')
        flat = stickers.ravel().tolist()
        if any(not isinstance(c, str) or c not in FACE_COLORS for c in flat):
            raise ValueError('Sticker colors must be W, O, G, R, B, or Y')
        if Counter(flat) != Counter({color: 9 for color in FACE_COLORS}):
            raise ValueError('Each color must appear exactly nine times')
        if tuple(stickers[:, 1, 1]) != FACE_COLORS:
            raise ValueError('Centers must be W, O, G, R, B, Y in U, L, F, R, B, D order')

        def decode(positions, kind):
            solved = [tuple(FACE_COLORS[index // 9] for index in piece)
                      for piece in positions]
            lookup = {}
            for piece_id, colors in enumerate(solved):
                for orientation in range(len(colors)):
                    lookup[colors[orientation:] + colors[:orientation]] = (piece_id, orientation)
            permutation, orientations = [], []
            for slot, indices in enumerate(positions):
                colors = tuple(flat[index] for index in indices)
                if colors not in lookup:
                    raise ValueError(f'Invalid or mirrored {kind} at slot {slot}: {colors}')
                piece, orientation = lookup[colors]
                permutation.append(piece)
                orientations.append(orientation)
            return permutation, orientations

        cp, co = decode(CORNER_FACELETS, 'corner')
        ep, eo = decode(EDGE_FACELETS, 'edge')
        return cls(cp, co, ep, eo)

    def to_solver_input(self):
        """The 40 integers expected by the C++ CLI: cp, co, ep, eo."""
        return '\n'.join(' '.join(map(str, values))
                         for values in (self.cp, self.co, self.ep, self.eo)) + '\n'
