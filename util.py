import pprint

import numpy as np
from amplify import sum_poly, gen_symbols, BinaryPoly

import cost
from file_reader import parse_test_case
from node import Node


def gen_random_tsp(ncity: int):
    nodes = []

    # Coordinate
    locations = np.random.uniform(size=(ncity, 2))

    # Distance matrix
    all_diffs = np.expand_dims(locations, axis=1) - np.expand_dims(locations, axis=0)
    distances = np.sqrt(np.sum(all_diffs ** 2, axis=-1))

    for i in range(ncity):
        n = Node(i + 1, tuple(locations[i]), ())
        nodes.append(n)

    return nodes, distances


def gen_solomon_tsp(ncity: int, path: str):
    nodes = parse_test_case(path)

    if ncity <= len(nodes):
        nodes = nodes[:ncity]

    locations = nodes_to_legacy_locations(nodes)

    # Distance matrix
    all_diffs = np.expand_dims(locations, axis=1) - np.expand_dims(locations, axis=0)
    distances = np.sqrt(np.sum(all_diffs ** 2, axis=-1))

    return nodes, distances


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
        temp[route[i] - 1] = 1
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


def nodes_to_legacy_locations(nodes):
    temp = []

    for n in nodes:
        temp.append(list(n.coordinates))

    locations = np.array(temp)

    return locations


def get_change(current, previous):
    if current == previous:
        return 0
    if current == 0 and previous != 0:
        return float('inf')
    if current != 0 and previous == 0:
        return float('inf')
    try:
        return round((abs(current - previous) / previous) * 100.0, 4)
    except ZeroDivisionError:
        return float('inf')
