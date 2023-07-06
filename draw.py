import os

import numpy as np
from matplotlib import pyplot as plt
from os import path

from util import nodes_to_legacy_locations


def show_plot(nodes):
    locations = nodes_to_legacy_locations(nodes)

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

def save_figure(route: list, distances: np.ndarray, locations: np.ndarray, test_file_path, time_limit, mode):
    ncity = len(route)

    path_length = round(sum(
        [distances[route[i]][route[(i + 1) % ncity]] for i in range(ncity)]), 4
    )

    x = [i[0] for i in locations]
    y = [i[1] for i in locations]
    plt.figure(figsize=(7, 7))
    plt.title(f"path length: {path_length}, " + f"ncity: {ncity}, " + f"time limit: {time_limit}, " + f"mode: {mode}")
    plt.xlabel("x")
    plt.ylabel("y")

    for i in range(ncity):
        r = route[i]
        n = route[(i + 1) % ncity]
        plt.plot([x[r], x[n]], [y[r], y[n]], "b-")
    plt.plot(x, y, "ro")

    filename_suffix = "plot_ncity_" + str(ncity) + "_t_" + str(time_limit) + "_" + mode +".png"

    if not test_file_path:
        filename = "random_generated_" + filename_suffix
    else:
        filename = str(test_file_path.rsplit('/', 1)[1])
        filename = filename.split('.')[0] + filename_suffix

    file_path = path.relpath("test_results/plots/" + filename)

    plt.savefig(file_path)

    plt.close()


