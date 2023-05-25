from amplify import sum_poly, BinaryPoly


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
