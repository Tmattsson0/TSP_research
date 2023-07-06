class Node:
    def __init__(self, number, coordinates, ready_time):
        self.number = number
        self.coordinates = coordinates
        self.ready_time = ready_time

    def __str__(self):
        return str(self.number) + ", " + str(self.coordinates)

    def __repr__(self):
        return str(self)