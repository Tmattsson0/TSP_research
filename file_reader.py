from node import Node


def parse_test_case(path):
    test_case = []

    f = open(path, 'r')

    temp = f.readlines()

    for i in range(9, len(temp)):
        line = temp[i]
        data = str.split(line)

        n = Node(data[0], (float(data[1]), float(data[2])), ())

        test_case.append(n)

    f.close()

    return test_case
