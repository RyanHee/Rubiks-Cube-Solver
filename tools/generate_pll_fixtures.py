"""Offline independent geometry check of diagram transcriptions; never imports Cube."""
import json
import re
from pathlib import Path

from PIL import Image
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
ALGORITHMS = {
    'Ub': "R2 U (R U R' U') R' U' (R' U R')",
    'Ua': "(R U' R U) R U (R U' R' U') R2",
    'Z': "(M2' U M2' U) (M' U2) (M2' U2 M') [U2]",
    'H': "(M2' U M2') U2 (M2' U M2')",
    'Aa': "x (R' U R') D2 (R U' R') D2 R2 x'",
    'Ab': "x R2' D2 (R U R') D2 (R U' R) x'",
    'E': "x' (R U' R' D) (R U R' D') (R U R' D) (R U' R' D') x",
    'Ra': "(R U' R' U') (R U R D) (R' U' R D') (R' U2 R') [U']",
    'Rb': "(R' U2 R U2') R' F (R U R' U') R' F' R2 [U']",
    'Ja': "(R' U L' U2) (R U' R' U2 R) L [U']",
    'Jb': "(R U R' F') (R U R' U') R' F R2 U' R' [U']",
    'T': "(R U R' U') (R' F R2 U') R' U' (R U R' F')",
    'F': "(R' U' F')(R U R' U')(R' F R2 U')(R' U' R U)(R' U R)",
    'V': "(R' U R' U') y (R' F' R2 U') (R' U R' F) R F",
    'Y': "F (R U' R' U') (R U R' F') (R U R' U') (R' F R F')",
    'Na': "(RUR'U)(RUR'F')(RUR'U')(R'FR2U') R' U2 (RU'R')",
    'Nb': "(R' U R U') (R' F' U' F) (R U R' F) R' F' (R U' R)",
    'Ga': "R2 U (R' U R' U') (R U' R2) D U' (R' U R D') [U]",
    'Gb': "(F' U' F) (R2 u R' U) (R U' R u') R2'",
    'Gc': "R2 U' (R U' R U) (R' U R2 D') (U R U' R') D [U']",
    'Gd': "D' (R U R' U') D (R2 U' R U') (R' U R' U) R2 [U]",
}
IMAGES = {
    'Ub': (0,22), 'Ua': (0,23), 'Z': (0,24), 'H': (0,25),
    'Aa': (0,21), 'Ab': (0,26), 'E': (0,27),
    'Ra': (1,34), 'Rb': (1,35), 'Ja': (1,36), 'Jb': (1,37),
    'T': (1,38), 'F': (1,39), 'V': (1,40), 'Y': (1,41),
    'Na': (1,42), 'Nb': (1,43), 'Ga': (1,30), 'Gb': (1,31),
    'Gc': (1,32), 'Gd': (1,33),
}
NORMALS = {'R': (1,0,0), 'L': (-1,0,0), 'U': (0,1,0),
           'D': (0,-1,0), 'F': (0,0,1), 'B': (0,0,-1)}
FACE_BY_NORMAL = {normal: face for face, normal in NORMALS.items()}
FACE_ORDER = 'ULFRBD'
COLORS = dict(zip(FACE_ORDER, 'WOGRBY'))


def rotate(v, axis, turns):
    x,y,z = v
    for _ in range(turns % 4):
        if axis == 'x': x,y,z = x,-z,y
        if axis == 'y': x,y,z = z,y,-x
        if axis == 'z': x,y,z = -y,x,z
    return x,y,z


def tokenize(algorithm):
    stripped = re.sub(r'[()\[\]\s]', '', algorithm)
    tokens = re.findall(r"[RLUDFBxyzMESrludfb](?:2'|2|')?", stripped)
    assert ''.join(tokens) == stripped
    return tokens


def outer_turns(algorithm):
    # Track regrips as a notation frame rather than physically rotating centers.
    frame = dict(NORMALS)
    result = []
    expansions = {'M': "x' R L'", 'E': "y' U D'", 'S': "z F' B",
                  'r': 'x L', 'l': "x' R", 'u': 'y D', 'd': "y' U",
                  'f': 'z B', 'b': "z' F"}

    def perform(token):
        base = token[0]
        n = 2 if '2' in token else (3 if "'" in token else 1)
        if base in NORMALS:
            physical = FACE_BY_NORMAL[frame[base]]
            result.append(physical + {1:'',2:'2',3:"'"}[n])
        elif base in 'xyz':
            old = frame.copy()
            for face, normal in NORMALS.items():
                frame[face] = old[FACE_BY_NORMAL[rotate(normal, base, n)]]
        else:
            for _ in range(n):
                for expanded in tokenize(expansions[base]):
                    perform(expanded)

    for token in tokenize(algorithm): perform(token)
    # Merge adjacent moves of the same face, including cancellation.
    simplified = []
    for token in result:
        n = 2 if '2' in token else (3 if "'" in token else 1)
        if simplified and simplified[-1][0] == token[0]:
            _, previous = simplified.pop()
            n = (n + previous) % 4
        if n: simplified.append((token[0], n))
    return ' '.join(face + {1:'',2:'2',3:"'"}[n] for face,n in simplified)


def sticker_geometry(face, r, c):
    return {'U': (c-1,1,r-1), 'D': (c-1,-1,1-r),
            'F': (c-1,1-r,1), 'B': (1-c,1-r,-1),
            'R': (1,1-r,1-c), 'L': (-1,1-r,c-1)}[face], NORMALS[face]


def geometric_start(algorithm):
    state = {sticker_geometry(face,r,c): COLORS[face]
             for face in FACE_ORDER for r in range(3) for c in range(3)}
    for token in reversed(algorithm.split()):
        face = token[0]
        count = 2 if '2' in token else (1 if "'" in token else 3)
        normal = NORMALS[face]
        index = next(i for i,n in enumerate(normal) if n)
        axis = 'xyz'[index]
        angle = -normal[index] * count
        state = {(rotate(pos,axis,angle),rotate(direction,axis,angle))
                 if pos[index] == normal[index] else (pos,direction): value
                 for (pos,direction),value in state.items()}
    return {face: [''.join(state[sticker_geometry(face,r,c)] for c in range(3))
                   for r in range(3)] for face in FACE_ORDER}


def diagram_colors(pdf, name):
    page,xref = IMAGES[name]
    rect = pdf[page].get_image_rects(xref)[-1]
    pix = pdf[page].get_pixmap(matrix=pymupdf.Matrix(4,4),clip=rect)
    im = Image.frombytes('RGB', (pix.width,pix.height),pix.samples)
    palette = {'R':(212,2,4),'O':(255,127,0),'G':(20,170,4),'B':(36,66,212)}
    sides = {}
    for side in 'BLFR':
        colors = []
        for t in (.18,.5,.82):
            x,y = {'B':(t,.035),'F':(t,.965),'L':(.035,t),'R':(.965,t)}[side]
            pixel = im.getpixel((int(x*(im.width-1)),int(y*(im.height-1))))
            color = min(palette, key=lambda c:sum((pixel[i]-palette[c][i])**2 for i in range(3)))
            assert sum((pixel[i]-palette[color][i])**2 for i in range(3)) < 10000, (name,side,pixel)
            colors.append(color)
        sides[side] = ''.join(colors)
    return sides


def verify_printed_algorithm(initial, algorithm):
    """Apply literal notation geometrically, without the outer-turn compiler."""
    state = {sticker_geometry(face,r,c): initial[face][r][c]
             for face in FACE_ORDER for r in range(3) for c in range(3)}
    for token in tokenize(algorithm):
        base = token[0]
        count = 2 if '2' in token else (3 if "'" in token else 1)
        if base in 'xyz':
            index = 'xyz'.index(base)
            sign = -1
            layers = {-1,0,1}
        elif base in 'MES':
            index,sign = {'M':(0,1),'E':(1,1),'S':(2,-1)}[base]
            layers = {0}
        else:
            normal = NORMALS[base.upper()]
            index = next(i for i,n in enumerate(normal) if n)
            sign = -normal[index]
            layers = {normal[index]}
            if base.islower(): layers.add(0)
        axis = 'xyz'[index]
        state = {(rotate(pos,axis,sign*count),rotate(direction,axis,sign*count))
                 if pos[index] in layers else (pos,direction): value
                 for (pos,direction),value in state.items()}
    # A printed regrip can change the final orientation; compare each face
    # with its own center, not with the original fixed color orientation.
    for face in FACE_ORDER:
        center = state[sticker_geometry(face,1,1)]
        assert all(state[sticker_geometry(face,r,c)] == center
                   for r in range(3) for c in range(3)), (algorithm,face)


def main():
    pdf = pymupdf.open(ROOT / 'pll-algorithms.pdf')
    cases = []
    for name,algorithm in ALGORITHMS.items():
        outer = outer_turns(algorithm)
        reference = geometric_start(outer)
        diagram = diagram_colors(pdf,name)
        color_map = {}
        for face,bar in diagram.items():
            row = bar[::-1] if face in 'BR' else bar
            for original,expected in zip(row,reference[face][0]):
                assert original not in color_map or color_map[original] == expected, (name,diagram,reference,color_map,original,expected)
                color_map[original] = expected
        assert set(color_map.values()) == set('OGRB')
        # The fixture comes from the diagram, not the algorithm or Cube's moves.
        initial = {face:[COLORS[face]*3]*3 for face in FACE_ORDER}
        for face,bar in diagram.items():
            row = bar[::-1] if face in 'BR' else bar
            initial[face][0] = ''.join(color_map[c] for c in row)
        assert initial == reference, (name,initial,reference)
        verify_printed_algorithm(initial, algorithm)
        cases.append({'name':name, 'algorithm':algorithm, 'outer_algorithm':outer,
                      'diagram_bars':diagram, 'diagram_color_map':color_map, 'initial_faces':initial})
        print(name, 'verified diagram', {f:initial[f][0] for f in 'LFRB'})
    output = {'source':'https://www.cubeskills.com/uploads/pdf/tutorials/pll-algorithms.pdf',
              'authors':['Feliks Zemdegs','Andy Klise'],
              'face_order':list(FACE_ORDER), 'solved_colors':COLORS, 'cases':cases}
    (ROOT / 'tests/fixtures/pll_cases.json').write_text(json.dumps(output,indent=2)+'\n')


if __name__ == '__main__':
    main()
