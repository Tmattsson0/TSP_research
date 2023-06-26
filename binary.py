import time

import numpy as np
import matplotlib.pyplot as plt
from amplify import BinaryPoly, gen_symbols, Solver, decode_solution, sum_poly
from amplify.constraint import equal_to
from amplify.client import FixstarsClient

from client import get_fixstars_client
from util import gen_random_tsp


def run_binary(seed, ncity, time_limit):
    try:
        np.random.seed(seed)

        locations, distances = gen_random_tsp(ncity)

        # show_plot(locations)

        q = gen_symbols(BinaryPoly, ncity, ncity)

        cost = sum_poly(
            ncity,
            lambda n: sum_poly(
                ncity,
                lambda i: sum_poly(
                    ncity, lambda j: distances[i][j] * q[n][i] * q[(n + 1) % ncity][j]
                ),
            ),
        )

        # print(cost)
        # Constraints on rows
        row_constraints = [
            equal_to(sum_poly([q[n][i] for i in range(ncity)]), 1) for n in range(ncity)
        ]

        # Constraints on columns
        col_constraints = [
            equal_to(sum_poly([q[n][i] for n in range(ncity)]), 1) for i in range(ncity)
        ]

        constraints = sum(row_constraints) + sum(col_constraints)

        constraints *= np.amax(distances)  # Set the strength of the constraint
        model = cost + constraints
        
        #Import 
        client = get_fixstars_client(time_limit)

        solver = Solver(client)

        result = solver.solve(model)

        if len(result) == 0:
            return 0
            raise RuntimeError("Any one of constraints is not satisfied.")

        print("Mode: Binary")
        print("Number of cities: " + str(ncity))
        print("Time limit: " + str(client.parameters.timeout))

        energy, values = result[0].energy, result[0].values

        q_values = decode_solution(q, values, 1)

        route = np.where(np.array(q_values) == 1)[1]

        # print(q_values)

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
