class Solver:
    def __init__(self, edges, cells_x, cells_y):
        self.edges = edges
        self.path = []
        self.cells_x = cells_x
        self.cells_y = cells_y
        self.begin = (0, 0)
        self.end = (cells_y - 1, cells_x - 1)
        self.dist = [[float('inf') for _ in range(self.cells_y)] for _ in range(self.cells_x)]
        self.solve()

    def solve(self):
        queue = [self.begin]
        self.dist[self.begin[0]][self.begin[1]] = 0
        exit_flag = False
        while len(queue) > 0 and not exit_flag:
            v = queue[0]
            del queue[0]
            if v in self.edges.keys():
                for to in self.edges[v]:
                    if self.dist[to[0]][to[1]] == float('inf'):
                        self.dist[to[0]][to[1]] = self.dist[v[0]][v[1]] + 1
                        queue.append(to)
                    if to == self.end:
                        exit_flag = True
                        break
        self.path.append(self.end)
        neighbour = self.get_neighbour(self.end, (self.cells_y, self.cells_x))
        while neighbour != self.begin:
            self.path.append(neighbour)
            neighbour = self.get_neighbour(neighbour, (self.cells_y, self.cells_x))
        self.path.append(self.begin)
        self.path = self.path[::-1]

    def get_neighbour(self, coords, borders):
        neighbors = [(i, j) for i, j in zip([coords[0] - 1, coords[0] + 1, coords[0], coords[0]],
                                            [coords[1], coords[1], coords[1] + 1, coords[1] - 1])]
        i = 0
        min_dist = float('inf')
        for coord in neighbors:
            if coord[0] >= 0 and coord[0] < borders[0] and coord[1] < borders[1] and coord[1] >= 0 and \
                    self.dist[coord[0]][
                        coord[1]] < min_dist and coord in self.edges.keys() and coords in self.edges[coord]:
                min_dist = self.dist[coord[0]][coord[1]]
        while i < len(neighbors):
            coord = neighbors[i]
            if coord[0] < 0 or coord[0] >= borders[0] or coord[1] >= borders[1] or coord[1] < 0 or self.dist[coord[0]][
                coord[1]] > min_dist or not (coord in self.edges.keys() and coords in self.edges[coord]):
                del neighbors[i]
            else:
                i += 1

        return neighbors[0]
