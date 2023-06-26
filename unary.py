import numpy as np
import cost as c
from amplify import BinaryPoly, gen_symbols, Solver, decode_solution
from amplify.client import FixstarsClient

from client import get_fixstars_client
from draw import show_route, show_plot
from util import gen_random_tsp


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

        client = get_fixstars_client(time_limit)

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
