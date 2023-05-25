import numpy as np
from amplify import sum_poly, gen_symbols, BinaryPoly

import cost


def gen_random_tsp(ncity: int):
    # Coordinate
    locations = np.random.uniform(size=(ncity, 2))

    # Distance matrix
    all_diffs = np.expand_dims(locations, axis=1) - np.expand_dims(locations, axis=0)
    distances = np.sqrt(np.sum(all_diffs ** 2, axis=-1))

    return locations, distances


def gen_test_tsp(ncity: int):
    np.random.seed(1)
    # Coordinate
    locations = np.random.uniform(size=(ncity, 2))

    # Distance matrix
    all_diffs = np.expand_dims(locations, axis=1) - np.expand_dims(locations, axis=0)
    distances = np.sqrt(np.sum(all_diffs ** 2, axis=-1))

    return locations, distances


def route_to_unary_dict(route: list):
    unary = []
    q_values = []
    q_dict = {}

    for i in route:
        for j in range(i):
            unary.append(1)
        temp = len(unary)
        for k in range(len(route) - temp):
            unary.append(0)
        q_values.extend(unary[1:])
        unary.clear()

    for j in range(len(route) * (len(route) - 1)):
        key_j = 'q_{}'.format(j)  # a string depending on j
        q_dict[key_j] = q_values[j]

    return q_dict


def route_to_binary_dict(route: list):
    q_values = []
    q_dict = {}

    for i in range(len(route)):
        temp = [0] * len(route)
        temp[i] = 1
        q_values.extend(temp)

    for j in range(len(route) * (len(route))):
        key_j = 'q_{}'.format(j)  # a string depending on j
        q_dict[key_j] = q_values[j]

    return q_dict


def qdict_to_qvalues(qdict: dict, q):

    temp = 0
    for i in range(len(q)):
        for j in range(len(q[0])):
            key_j = 'q_{}'.format(temp)  # a string depending on j
            q[i][j] = qdict.get(key_j)
            temp = temp + 1

    return q


# test = "- 0.466811 q_0 q_2 + 0.465021 q_0 q_3 - 0.466811 q_0 q_4 + 0.465021 q_0 q_5 + 0.465021 q_1 q_2 - 0.916739 q_1 q_3 + 0.465021 q_1 q_4 - 0.916739 q_1 q_5 - 0.466811 q_2 q_4 + 0.465021 q_2 q_5 + 0.465021 q_3 q_4 - 0.916739 q_3 q_5 + 0.466811 q_0 - 0.0133025 q_1 + 0.466811 q_2 - 0.0133025 q_3 + 0.466811 q_4 - 0.0133025 q_5"
#
# _, dist = gen_test_tsp(3)
# q = gen_symbols(BinaryPoly, 3, 3 - 1)  # Example for 32 cities. Binary change to unary
#
# test2 = cost.cost_func_unary(dist, q, 3)
#
#
# qdict = route_to_unary_dict([1, 2, 3])
#
# qdict_to_qvalues(test2, qdict)