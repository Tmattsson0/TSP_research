from os import path

import binary
import unary
from util import get_change

seed = 0
ncity = 0
ns = [5, 10, 25, 50]
time_limit = 0
temp_u = []
temp_b = []
failed_runs = []

filename = "random_generated_avg.txt"
file_path = path.relpath("test_results/" + filename)
f = open(file_path, "w")

for n in ns:
    for i in range(1, 11):
        for seed in range(10):
            run_temp = unary.run_unary(seed, n, i * 1000, "")
            if run_temp != 0:
                temp_u.append(run_temp)
            elif run_temp == 0:
                run = ("u", i, n, seed)
                failed_runs.append(run)
                continue

            run_temp = binary.run_binary(seed, n, i*1000, "")
            if run_temp != 0:
                temp_b.append(run_temp)
            elif run_temp == 0:
                run = ("b", i, n, seed)
                failed_runs.append(run)
                temp_u.pop()
                continue

        f.write("Ncity: " + str(n) + ", time limit: " + str(i*1000) + "\n")
        if len(temp_u) == 0 or len(temp_b) == 0:
            f.write("Unary avg length: " + str(0) + "\n")
            f.write("Binary avg length: " + str(0) + "\n")
        else:
            f.write("Unary avg length: " + str(round(sum(temp_u) / len(temp_u), 4)) + "\n")
            f.write("Binary avg length: " + str(round(sum(temp_b) / len(temp_b), 4)) + "\n")
            f.write("Difference: " + str(get_change(sum(temp_u) / len(temp_u), sum(temp_b) / len(temp_b))) + "\n")

        f.write("Failed runs: ")
        f.write(str(failed_runs))
        f.write("\n")
        f.write("\n")

        failed_runs.clear()
        temp_u.clear()
        temp_b.clear()
        