import numpy as np
import cost as c
from amplify import BinaryPoly, gen_symbols, Solver, decode_solution
from amplify.client import FixstarsClient

import draw
from client import get_fixstars_client
from draw import show_route, show_plot
from util import gen_random_tsp, gen_solomon_tsp, nodes_to_legacy_locations


def run_unary(seed, ncity, time_limit, test_file_path):
    try:
        np.random.seed(seed)

        # nodes, distances = gen_random_tsp(ncity)
        nodes, distances = gen_solomon_tsp(ncity, test_file_path)

        # show_plot(nodes)

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
            print("Any one of constraints is not satisfied.")
            return 0

        print("Mode: Unary")
        print("Number of cities: " + str(ncity))
        print("Time limit: " + str(client.parameters.timeout))

        energy, values = result[0].energy, result[0].values

        q_values = decode_solution(q, values, 1)

        # print(q_values)

        route = np.count_nonzero(q_values > 0, axis=1)  # Count number of 1's in each row.

        print("Route: " + str(route))

        # show_route(route, distances, nodes_to_legacy_locations(nodes))
        draw.save_figure(route, distances, nodes_to_legacy_locations(nodes), test_file_path, ncity, time_limit, "unary")

        print("Path length: " + str(round(sum(
            [distances[route[i]][route[(i + 1) % ncity]] for i in range(ncity)]
        )
        , 4)) + "\n")

        return round(sum(
            [distances[route[i]][route[(i + 1) % ncity]] for i in range(ncity)]
        ), 4)

    # Fixstars client throws RuntimeWarnings, this exception is to allow for the experiment to run after warnings are
    # thrown.
    except RuntimeWarning:
        print("Failed because of RuntimeWarning")
        return 0
