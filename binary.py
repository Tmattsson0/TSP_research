import time

import numpy as np
import matplotlib.pyplot as plt
from amplify import BinaryPoly, gen_symbols, Solver, decode_solution, sum_poly
from amplify.constraint import equal_to
from amplify.client import FixstarsClient

np.random.seed(1)

def gen_random_tsp(ncity: int):
    # Coordinate
    locations = np.random.uniform(size=(ncity, 2))

    # Distance matrix
    all_diffs = np.expand_dims(locations, axis=1) - np.expand_dims(locations, axis=0)
    distances = np.sqrt(np.sum(all_diffs ** 2, axis=-1))

    return locations, distances


def show_plot(locs: np.ndarray):
    plt.figure(figsize=(7, 7))
    plt.xlabel("x")
    plt.ylabel("y")
    plt.scatter(*zip(*locations))
    plt.show()


ncity = 32
locations, distances = gen_random_tsp(ncity)

show_plot(locations)

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

# Set Ising Machine Client Settings
client = FixstarsClient()
client.token = "IcrKdmn7sqNjqZqjCIbRlzrFlhnrEQoW"
client.parameters.timeout = 7000

solver = Solver(client)

start = time.time()

result = solver.solve(model)

if len(result) == 0:
    raise RuntimeError("Any one of constraints is not satisfied.")

end = time.time()
print("Number of cities: " + str(ncity))
print("Time: " + str(end - start))

energy, values = result[0].energy, result[0].values

q_values = decode_solution(q, values, 1)

route = np.where(np.array(q_values) == 1)[1]

print(q_values)

print("Route: " + str(route))

def show_route(route: list, distances: np.ndarray, locations: np.ndarray):
    ncity = len(route)
    path_length = sum(
        [distances[route[i]][route[(i + 1) % ncity]] for i in range(ncity)]
    )

    x = [i[0] for i in locations]
    y = [i[1] for i in locations]
    plt.figure(figsize=(7, 7))
    plt.title(f"path length: {path_length}")
    plt.xlabel("x")
    plt.ylabel("y")

    for i in range(ncity):
        r = route[i]
        n = route[(i + 1) % ncity]
        plt.plot([x[r], x[n]], [y[r], y[n]], "b-")
    plt.plot(x, y, "ro")
    plt.show()

    return path_length


show_route(route, distances, locations)

print("Path length: " + str(sum(
        [distances[route[i]][route[(i + 1) % ncity]] for i in range(ncity)]
    )
))