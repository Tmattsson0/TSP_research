import time

import numpy as np
import cost as c
import matplotlib.pyplot as plt
from amplify import BinaryPoly, gen_symbols, Solver, decode_solution, sum_poly, BinaryIntPoly
from amplify.constraint import equal_to, greater_equal
from amplify.client import FixstarsClient


def gen_random_tsp(ncity: int):
    # Coordinate
    locations = np.random.uniform(size=(ncity, 2))

    # Distance matrix
    all_diffs = np.expand_dims(locations, axis=1) - np.expand_dims(locations, axis=0)
    distances = np.sqrt(np.sum(all_diffs ** 2, axis=-1))

    return locations, distances


def show_plot(locations: np.ndarray):
    plt.figure(figsize=(7, 7))
    plt.xlabel("x")
    plt.ylabel("y")
    plt.scatter(*zip(*locations))
    plt.show()


def show_route(route: list, distances: np.ndarray, locations: np.ndarray):
    ncity = len(route)
    path_length = round(sum(
        [distances[route[i]][route[(i + 1) % ncity]] for i in range(ncity)]), 4
    )

    # x = [i[0] for i in locations]
    # y = [i[1] for i in locations]
    # plt.figure(figsize=(7, 7))
    # plt.title(f"path length: {path_length}")
    # plt.xlabel("x")
    # plt.ylabel("y")
    #
    # for i in range(ncity):
    #     r = route[i]
    #     n = route[(i + 1) % ncity]
    #     plt.plot([x[r], x[n]], [y[r], y[n]], "b-")
    # plt.plot(x, y, "ro")
    # plt.show()

    return path_length


def run_unary(seed, ncity, time_limit):
    try:
        np.random.seed(seed)

        locations, distances = gen_random_tsp(ncity)

        # show_plot(locations)

        q = gen_symbols(BinaryPoly, ncity, ncity - 1)

        cost = c.cost_func_unary_v2(distances, q, ncity)

        # row_constraints = c.row_constraint_unary(q, ncity)

        col_constraints = c.col_constraint_unary(q, ncity)

        # constraints = sum(row_constraints) + sum(col_constraints)
        constraints = sum(col_constraints)

        constraints *= np.amax(distances)  # Set the strength of the constraint

        model = cost + constraints

        # Set Ising Machine Client Settings
        client = FixstarsClient()
        client.token = "IcrKdmn7sqNjqZqjCIbRlzrFlhnrEQoW"
        client.parameters.timeout = time_limit  # Timeout is 5 seconds

        solver = Solver(client)

        result = solver.solve(model)

        if len(result) == 0:
            return 0

        print("Mode: Unary")
        print("Number of cities: " + str(ncity))
        print("Time limit: " + str(client.parameters.timeout))

        energy, values = result[0].energy, result[0].values

        q_values = decode_solution(q, values, 1)

        # print(q_values)

        route = np.count_nonzero(q_values > 0, axis=1)  # Count number of 1's in each row.

        print("Route: " + str(route))

        # show_route(route, distances, locations)

        print("Path length: " + str(round(sum(
            [distances[route[i]][route[(i + 1) % ncity]] for i in range(ncity)]
        )
        , 4)) + "\n")

        return round(sum(
            [distances[route[i]][route[(i + 1) % ncity]] for i in range(ncity)]
        ), 4)

    except RuntimeWarning:
        print("I failed")
        return 0