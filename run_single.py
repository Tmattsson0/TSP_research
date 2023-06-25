import binary
import unary


def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')

n = 4
time_limit = 1000
seed = 5
ns = [4, 8, 16, 32, 64, 128]


run_temp_u = unary.run_unary(seed, n, time_limit)
run_temp_b = binary.run_binary(seed, n, time_limit)

print(run_temp_u)
print(run_temp_b)



# print("\n")
# print("Ncity: " + str(n) + ", time limit: " + str(i * 1000) + "\n")
# print("Unary avg length: " + str(sum(temp_u) / len(temp_u)) + "\n")
# print("Binary avg length: " + str(sum(temp_b) / len(temp_b)) + "\n")
# print("Difference: " + str(get_change(sum(temp_u) / len(temp_u), sum(temp_b) / len(temp_b))) + "\n")