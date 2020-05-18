import numpy as np


corner_colours = [(0, 2, 5), (0, 3, 5), (0, 2, 4), (0, 3, 4), (1, 2, 5), (1, 3, 5), (1, 2, 4), (1, 3, 4)]
corner_ids = None
corner_assign_table = None
corner_position_table = None


def make_corner_ids():
    res = dict()

    for i in range(len(corner_colours)):
        res[corner_colours[i]] = i

    return res

corner_ids = make_corner_ids()

def make_corner_assign_table():
    x = -1

    return np.array(
          [[[0, x, 1],
            [x, x, x],
            [2, x, 3]],

           [[5, x, 4],
            [x, x, x],
            [7, x, 6]],

           [[4, x, 0],
            [x, x, x],
            [6, x, 2]],

           [[7, x, 3],
            [x, x, x],
            [5, x, 1]],

           [[6, x, 2],
            [x, x, x],
            [7, x, 3]],

           [[5, x, 1],
            [x, x, x],
            [4, x, 0]]])

corner_assign_table = make_corner_assign_table()

def make_corner_position_table():
    return [sorted([tuple(place) for place in np.transpose(np.where(corner_assign_table == i))]) for i in range(len(corner_colours))]

corner_position_table = make_corner_position_table()

edge_colours = [(0, 5), (0, 2), (0, 3), (0, 4), (2, 5), (3, 5), (2, 4), (3, 4), (1, 5), (1, 2), (1, 3), (1, 4)]
edge_ids = None
edge_assign_table = None
edge_position_table = None


def make_edge_ids():
    res = dict()

    for i in range(len(edge_colours)):
        res[edge_colours[i]] = i

    return res

edge_ids = make_edge_ids()

def make_edge_assign_table():
    x = -1

    return np.array(
          [[[ x,  0,  x],
            [ 1,  x,  2],
            [ x,  3,  x]],

           [[ x,  8,  x],
            [10,  x,  9],
            [ x, 11,  x]],

           [[ x,  4,  x],
            [ 9,  x,  1],
            [ x,  6,  x]],

           [[ x,  7,  x],
            [10,  x,  2],
            [ x,  5,  x]],

           [[ x,  6,  x],
            [11,  x,  3],
            [ x,  7,  x]],

           [[ x,  5,  x],
            [ 8,  x,  0],
            [ x,  4,  x]]])

edge_assign_table = make_edge_assign_table()

def make_edge_position_table():
    return [sorted([tuple(place) for place in np.transpose(np.where(edge_assign_table == i))]) for i in range(len(edge_colours))]

edge_position_table = make_edge_position_table()


def convert_basic_to_reduced(obs):
    res = np.zeros((20, 24), dtype=np.float)

    for i in range(len(corner_colours)):
        position = corner_position_table[i]
        colours = [obs[place] for place in position]
        colours_sorted = tuple(sorted(colours))
        id = corner_ids[colours_sorted]
        res[id, 3 * i + np.argmin(colours)] = 1.

    for i in range(len(edge_colours)):
        position = edge_position_table[i]
        colours = [obs[place] for place in position]
        colours_sorted = tuple(sorted(colours))
        id = edge_ids[colours_sorted]
        res[len(corner_colours) + id, 2 * i + np.argmin(colours)] = 1.

    return res

# corner_colours = [(0, 2, 5), (0, 3, 5), (0, 2, 4), (0, 3, 4), (1, 2, 5), (1, 3, 5), (1, 2, 4), (1, 3, 4)]
is_natural =       [  False,     True ,     True ,     False,     True,     False,     False,     True  ]

def convert_reduced_to_basic(obs):
    res = np.zeros((6, 3, 3), dtype=np.float32)

    for i in range(len(corner_colours)):
        idx = np.where(obs[i] == 1)[0][0]
        place = idx // 3
        rotation = idx % 3
        colors = corner_colours[i]
        colors_rotated = [0, 0, 0]
        colors_rotated[rotation] = colors[0]
        if is_natural[i] ^ is_natural[place]:
            colors_rotated[(rotation + 1) % 3] = colors[2]
            colors_rotated[(rotation + 2) % 3] = colors[1]
        else:
            colors_rotated[(rotation + 1) % 3] = colors[1]
            colors_rotated[(rotation + 2) % 3] = colors[2]

        for k, pos in enumerate(corner_position_table[place]):
            res[pos] = colors_rotated[k]
        # print(i, idx, place, rotation, colors, colors_rotated)

    for i in range(len(edge_colours)):
        idx = np.where(obs[i + len(corner_colours)] == 1)[0][0]
        place = idx // 2
        rotation = idx % 2
        colors = edge_colours[i]
        colors_rotated = (colors + colors + colors)[2 - rotation : 4 - rotation]
        for k, pos in enumerate(edge_position_table[place]):
            res[pos] = colors_rotated[k]
        # print(i, idx, place, rotation, colors, colors_rotated)

    for i in range(6):
        res[i, 1, 1] = i

    return res


# print(corner_colours)
# print(corner_ids)
# print(corner_assign_table)
# print(corner_position_table)


from gym_rubik.envs.cube import Actions, Cube

cube = Cube(3, whiteplastic=False)
# print(convert_basic_to_reduced(cube.get_state()))
# print(convert_reduced_to_basic(convert_basic_to_reduced(cube.get_state())))

ACTION_LOOKUP = {
    0: Actions.U,
    1: Actions.U_1,
    2: Actions.D,
    3: Actions.D_1,
    4: Actions.F,
    5: Actions.F_1,
    6: Actions.B,
    7: Actions.B_1,
    8: Actions.R,
    9: Actions.R_1,
    10: Actions.L,
    11: Actions.L_1
}

cube = Cube(3, whiteplastic=False)
cube.move_by_action(ACTION_LOOKUP[10])
print("TESTING")
print(convert_basic_to_reduced(cube.get_state()))
print(cube.get_state())
print(convert_reduced_to_basic(convert_basic_to_reduced(cube.get_state())))

import sys

for i in range(1000):
    cube = Cube(3, whiteplastic=False)
    for _ in range(100):
        cube.move_by_action(ACTION_LOOKUP[np.random.randint(0, 12)])
    print(cube.get_state())

    if not np.array_equal(cube.get_state(), convert_reduced_to_basic(convert_basic_to_reduced(cube.get_state()))):
        print("TESTING FAILED")
        print(convert_basic_to_reduced(cube.get_state()))
        print(cube.get_state())
        print(convert_reduced_to_basic(convert_basic_to_reduced(cube.get_state())))
        sys.exit(0)
    
print("TESTING OK")