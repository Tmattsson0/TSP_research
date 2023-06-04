from amplify import sum_poly, BinaryPoly
from amplify.amplify.constraint import equal_to, greater_equal


def cost_func_unary(distances, q, ncity):
    costs = []

    for i in range(ncity):  # Should be sumpoly(ncity, ?)
        for j in range(-1, ncity - 1):
            for j_prime in range(-1, ncity - 1):

                if j == j_prime:
                    f = BinaryPoly(0)
                    costs.append(f)

                if (0 <= j <= ncity - 3) and (j_prime == -1):
                    f = BinaryPoly(distances[j + 1][0] * (q[i][j] - q[i][j + 1]) * (1 - q[(i + 1) % ncity][0]))
                    costs.append(f)

                if (j == ncity - 2) and (j_prime == -1):
                    f = BinaryPoly(distances[ncity - 1][0] * q[i][ncity - 2] * (1 - q[(i + 1) % ncity][0]))
                    costs.append(f)

                if (j == -1) and (0 <= j_prime <= ncity - 3):
                    f = BinaryPoly(distances[0][j_prime + 1] * (1 - q[i][0]) * (
                            q[(i + 1) % ncity][j_prime] - q[(i + 1) % ncity][j_prime + 1]))
                    costs.append(f)

                if (0 <= j <= ncity - 3) and (0 <= j_prime <= ncity - 3):
                    f = BinaryPoly(distances[j + 1][j_prime + 1] * (q[i][j] - q[i][j + 1]) * (
                            q[(i + 1) % ncity][j_prime] - q[(i + 1) % ncity][j_prime + 1]))
                    costs.append(f)

                if (j == ncity - 2) and (0 <= j_prime <= ncity - 3):
                    f = BinaryPoly(distances[ncity - 1][j_prime + 1] * q[i][ncity - 2] * (
                            q[(i + 1) % ncity][j_prime] - q[(i + 1) % ncity][j_prime + 1]))
                    costs.append(f)

                if (j == -1) and (j_prime == ncity - 2):
                    f = BinaryPoly(distances[0][ncity - 1] * (1 - q[i][0]) * q[(i + 1) % ncity][ncity - 2])
                    costs.append(f)

                if (0 <= j <= ncity - 3) and (j_prime == ncity - 2):
                    f = BinaryPoly(
                        distances[j + 1][ncity - 1] * (q[i][j] - q[i][j + 1]) * q[(i + 1) % ncity][ncity - 2])
                    costs.append(f)
    cost = sum_poly(costs)
    return cost


def cost_func_binary(distances, q, ncity):
    cost = sum_poly(
        ncity,
        lambda n: sum_poly(
            ncity,
            lambda i: sum_poly(
                ncity, lambda j: distances[i][j] * q[n][i] * q[(n + 1) % ncity][j]
            ),
        ),
    )

    return cost


def col_constraint_binary(q, ncity):
    return [equal_to(sum_poly([q[n][i] for n in range(ncity)]), 1) for i in range(ncity)]


def col_constraint_unary(q, ncity):
    col_constraints_unary = [
        equal_to(sum_poly([q[i][j] - q[i][j + 1] for i in range(ncity)]), 1) for j in range(ncity - 2)
    ]

    edge_cost = equal_to(sum_poly([q[i][ncity - 2] for i in range(ncity)]), 1)

    col_constraints_unary.append(edge_cost)

    return col_constraints_unary


def row_constraint_unary(q, ncity):
    row_constraints = [
        greater_equal(sum_poly([q[i][j] - q[i][j + 1] for i in range(ncity - 1)]), 0) for j in range(ncity - 2)
    ]

    return row_constraints

# row_constraints = [
#     equal_to(sum_poly([q[n][i] for i in range(ncity)]), 1) for n in range(ncity)
# ]
