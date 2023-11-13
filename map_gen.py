import random
import sys


class Generator:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.visited = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.map = [[1 for _ in range(self.width * 3)] for _ in range(self.height * 3)]
        self.passes = {}

    def dfs(self):
        coords = (0, 0)
        self.visited[coords[0]][coords[1]] = 1
        queue = [coords]

        while len(queue) > 0:
            self.visited[coords[0]][coords[1]] = 1
            available_neighbours = self.get_neighbours(coords, (self.height, self.width),
                                                       lambda coord: self.visited[coord[0]][coord
                                                       [1]] == 1)

            if len(available_neighbours) == 0:
                del queue[-1]
                if len(queue) > 0:
                    coords = queue[-1]
                continue

            direction = random.randint(0, len(available_neighbours) - 1)
            neighbour = available_neighbours[direction]

            if self.visited[neighbour[0]][neighbour[1]] == 0:
                self.add_pass(coords, neighbour)
                queue.append(neighbour)
                coords = neighbour
                continue

    def aldous_broder(self):
        coords = (0, 0)
        not_visited = self.width * self.height
        while not_visited > 0:
            neighbours = self.get_neighbours(coords, (self.height, self.width))
            rand_dir = random.randint(0, len(neighbours) - 1)
            neighbour = neighbours[rand_dir]

            if self.visited[neighbour[0]][neighbour[1]] == 0:
                self.add_pass(coords, neighbour)
                self.visited[neighbour[0]][neighbour[1]] = 1
                not_visited -= 1
                coords = neighbour

            else:
                yes_no = random.randint(0, 50)
                if yes_no == 1:
                    self.add_pass(coords, neighbour)
                coords = neighbour

    def kruskal(self):
        groups = {(j, i): i * self.width + j for i in range(self.width) for j in range(self.height)}
        edges = self.create_random_passes()
        for edge in edges:
            if groups[edge[0]] != groups[edge[1]]:
                self.add_pass(edge[0], edge[1])
                self.add_pass(edge[1], edge[0])
                for v in groups.keys():
                    if groups[v] == groups[edge[1]]:
                        groups[v] = groups[edge[0]]

    def create_random_passes(self):
        edges = []
        for i in range(self.height):
            for j in range(self.width):
                neighbours = self.get_neighbours((i, j), (self.height, self.width))
                for neighbour in neighbours:
                    edges.append(((i, j), neighbour))
                    edges.append((neighbour, (i, j)))
        random.shuffle(edges)
        return edges

    def get_neighbours(self, coords, borders, condition_manager=(lambda coord: False)):
        neighbors = [(i, j) for i, j in zip([coords[0] - 1, coords[0] + 1, coords[0], coords[0]],
                                            [coords[1], coords[1], coords[1] + 1, coords[1] - 1])]
        i = 0
        while i < len(neighbors):
            coord = neighbors[i]
            if coord[0] < 0 or coord[0] >= borders[0] or coord[1] >= borders[1] or coord[1] < 0 or condition_manager(
                    coord):
                del neighbors[i]
            else:
                i += 1

        return neighbors

    def generate_map(self):
        for v in self.passes.keys():
            for to in self.passes[v]:
                if v[0] == to[0]:
                    start = min(v[1], to[1])
                    end = max(v[1], to[1])
                    for i in range(1 + 3 * start, 1 + 3 * end + 1):
                        self.map[1 + 3 * v[0]][i] = 0
                elif v[1] == to[1]:
                    start = min(v[0], to[0])
                    end = max(v[0], to[0])
                    for i in range(1 + 3 * start, 1 + 3 * end + 1):
                        self.map[i][1 + 3 * v[1]] = 0

    def add_pass(self, coords, neighbour):
        if coords not in self.passes.keys():
            self.passes[coords] = []
        self.passes[coords].append(neighbour)
