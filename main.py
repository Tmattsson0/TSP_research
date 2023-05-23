import numpy as np
import matplotlib.pyplot as plt
from amplify import BinaryPoly, gen_symbols, Solver, decode_solution, sum_poly
from amplify.constraint import equal_to, greater_equal
from amplify.client import FixstarsClient


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


ncity = 4
locations, distances = gen_random_tsp(ncity)

show_plot(locations)

q = gen_symbols(BinaryPoly, ncity, ncity - 1)  # Example for 32 cities. Binary change to unary

# q_4city = gen_symbols(BinaryPoly, 4, 4) # Example for four cities. Binary change to unary

cost = sum_poly(
    ncity,
    lambda n: sum_poly(
        ncity,
        lambda i: sum_poly(
            ncity, lambda j: distances[i][j] * q[n][i] * q[(n + 1) % ncity][j]
        ),
    ),
)

# cost_unary = sum_poly(
#     ncity,
#     lambda n: sum_poly(
#         ncity,
#         lambda i: sum_poly(
#             ncity - 1, lambda j: distances[i][j] * q[n][i] * q[(n + 1) % ncity][j]
#         ),
#     ),
# )

costs = []

for i in range(ncity): # Should be sumpoly(ncity, ?)
    for j in range(-1, ncity - 1):
        for j_prime in range(-1, ncity - 1):

            if (j is -1 and j_prime is -1) or (j is ncity - 2 and j_prime is ncity - 2):
                #Should be if (j == j_prime)
                f = 0
                costs.append(f)

            if (0 <= j <= ncity - 3) and (j_prime == -1):
                f = distances[j][0] * (q[i][j] - q[i][j + 1]) * (1 - q[i + 1][0])
                costs.append(f)

            if (j == ncity - 2) and (j_prime == -1):
                f = distances[ncity - 2][0] * q[i][ncity - 2] * (1 - q[i + 1][0])
                costs.append(f)

            if (j == -1) and (0 <= j_prime <= ncity - 3):
                f = distances[0][j_prime] * (1 - q[i][0]) * (q[i+1][j_prime] - q[i + 1][j_prime + 1])
                costs.append(f)

            if (0 <= j <= ncity - 3) and (0 <= j_prime <= ncity - 3):
                f = distances[j][j_prime] * (q[i][j] - q[i][j + 1]) * (q[i + 1][j_prime] - q[i + 1][j_prime + 1])
                costs.append(f)

            if (j == ncity - 2) and (0 <= j_prime <= ncity - 3):
                f = distances[ncity - 2][j_prime] * q[i][ncity - 2] * (q[i + 1][j_prime] - q[i + 1][j_prime + 1])
                costs.append(f)

            if (j == -1) and (j_prime == ncity - 2):
                f = distances[0][ncity - 2] * (1 - q[i][0]) * q[i + 1][ncity - 2]
                costs.append(f)

            if (0 <= j <= ncity - 3) and (j_prime == ncity - 2):
                f = distances[j][ncity - 2] * (q[i][j] - q[i][j + 1]) * q[i + 1][ncity - 2]
                costs.append(f)


c = sum_poly(costs[i] for i in range(len(costs)))

print(c)


for stuff in q:
    print("this is stuff " + str(stuff))

print(cost)


# Constraints on rows
row_constraints = [
    equal_to(sum_poly([q[n][i] for i in range(ncity)]), 1) for n in range(ncity)
]

# row_constraints_modified = [
#     greater_equal(q[i][j],q[i][j+1]) for i in range(ncity), for j in range(ncity-1)
# ]

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
client.parameters.timeout = 5000  # Timeout is 5 seconds

solver = Solver(client)

result = solver.solve(model)
if len(result) == 0:
    raise RuntimeError("Any one of constraints is not satisfied.")

energy, values = result[0].energy, result[0].values

q_values = decode_solution(q, values, 1)

print(q_values)

route = np.where(np.array(q_values) == 1)[1]
print(route)


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
