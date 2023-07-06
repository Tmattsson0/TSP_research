import numpy as np
from amplify import BinaryPoly, gen_symbols, Solver, decode_solution, sum_poly
from amplify.constraint import equal_to

import draw
from client import get_fixstars_client
from util import gen_random_tsp, gen_solomon_tsp, nodes_to_legacy_locations


def run_binary(seed, ncity, time_limit, test_file_path):
    try:
        np.random.seed(seed)

        if not test_file_path:
            nodes, distances = gen_random_tsp(ncity)
        else:
            nodes, distances = gen_solomon_tsp(ncity, test_file_path)

        # show_plot(nodes)

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
            print("Any one of constraints is not satisfied.")
            return 0

        print("Mode: Binary")
        print("Number of cities: " + str(ncity))
        print("Time limit: " + str(client.parameters.timeout))

        energy, values = result[0].energy, result[0].values

        q_values = decode_solution(q, values, 1)

        route = np.where(np.array(q_values) == 1)[1]

        # print(q_values)

        print("Route: " + str(route))

        # show_route(route, distances, nodes_to_legacy_locations(nodes))
        draw.save_figure(route, distances, nodes_to_legacy_locations(nodes), test_file_path, time_limit, "binary")

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
