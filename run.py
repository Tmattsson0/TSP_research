import time

import binary
import unary

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return round((abs(current - previous) / previous) * 100.0, 4)
    except ZeroDivisionError:
        return float('inf')

seed = 0
ncity = 0
ns = [4, 8, 16, 32, 64]
# ns = [4, 8, 16]
time_limit = 0

temp_u = []
temp_b = []
failed_runs = []

f = open("tests.txt", "w")

for i in range(1, 6):
    for n in ns:
        for seed in range(10):
            run_temp = unary.run_unary(seed, n, i * 1000)
            if run_temp != 0:
                temp_u.append(run_temp)
            elif run_temp == 0:
                run = ("u", i, n, seed)
                failed_runs.append(run)
                continue
            # time.sleep(2)

            run_temp = binary.run_binary(seed, n, i*1000)
            if run_temp != 0:
                temp_b.append(run_temp)
            elif run_temp == 0:
                run = ("b", i, n, seed)
                failed_runs.append(run)
                temp_u.pop()
                continue
            # time.sleep(2)

        f.write("\n")
        f.write("Ncity: " + str(n) + ", time limit: " + str(i*1000) + "\n")
        if len(temp_u) == 0 or len(temp_b) == 0:
            f.write("Unary avg length: " + str(0) + "\n")
            f.write("Binary avg length: " + str(0) + "\n")
        else:
            f.write("Unary avg length: " + str(round(sum(temp_u) / len(temp_u), 4)) + "\n")
            f.write("Binary avg length: " + str(round(sum(temp_b) / len(temp_b), 4)) + "\n")
            f.write("Difference: " + str(get_change(sum(temp_u) / len(temp_u), sum(temp_b) / len(temp_b))) + "\n")
        f.write(str(failed_runs))
        failed_runs.clear()
        temp_u.clear()
        temp_b.clear()