import os
from os import path

import binary
import unary
from util import get_change

seed = 0
ncity = 0
# ns = [4, 8, 16, 32, 64]
ns = [5, 10, 25, 50]
time_limit = 0
temp_u = 0
temp_b = 0
run_u = None
run_b = None
failed_runs = []

mypath = "/Users/thomasmattsson/Documents/GitHub/TSP_research/test_cases_small"
paths = [os.path.join(dirpath, f) for (dirpath, dirnames, filenames) in os.walk(mypath) for f in filenames]
paths.sort()

for p in paths:
    filename = str(p.rsplit('/', 1)[1])
    filename = filename.split('.')[0] + "_test.txt"
    file_path = path.relpath("test_results/" + filename)
    f = open(file_path, "w")

    for n in ns:
        for i in range(1, 11):
            temp_u = unary.run_unary(0, n, i * 1000, p)
            if temp_u != 0:
                run_u = temp_u
            elif temp_u == 0:
                run = ("u", i, n, 0)
                failed_runs.append(run)

            temp_b = binary.run_binary(0, n, i * 1000, p)
            if temp_b != 0:
                run_b = temp_b
            elif temp_b == 0:
                run = ("b", i, n, 0)
                failed_runs.append(run)

            f.write("Ncity: " + str(n) + ", time limit: " + str(i * 1000) + "\n")

            if run_u is None and run_b is None:
                f.write("Unary length: " + str(0) + "\n")
                f.write("Binary length: " + str(0) + "\n")
                f.write("Difference: " + str(get_change(0, 0)) + "\n")

            elif run_u is None and run_b is not None:
                f.write("Unary length: " + str(0) + "\n")
                f.write("Binary length: " + str(run_b) + "\n")
                f.write("Difference: " + str(get_change(0, run_b)) + "\n")

            elif run_u is not None and run_b is None:
                f.write("Unary length: " + str(run_u) + "\n")
                f.write("Binary length: " + str(0) + "\n")
                f.write("Difference: " + str(get_change(run_u, 0)) + "\n")

            else:
                f.write("Unary length: " + str(run_u) + "\n")
                f.write("Binary length: " + str(run_b) + "\n")
                f.write("Difference: " + str(get_change(run_u, run_b)) + "\n")

            f.write("Failed runs:")
            f.write(str(failed_runs))

            f.write("\n")
            f.write("\n")

            failed_runs.clear()
            run_u = 0
            run_b = 0
