import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import colors
from collections import deque
import glob

class Agent:
    def __init__(self):
        self.actions = [
            (0,-1),
            (1,-1),
            (1,0), 
            (1,1),
            (0,1),
            (-1,1),
            (-1,0),
            (-1,-1)
        ]

    def set_position(self, env):
        self.pos = None
        while not self.pos:
            num_rows = env.num_rows
            num_cols = env.num_cols
            choice = (random.randint(0, num_rows-1), random.randint(0, num_cols-1))
            if choice not in env.obstacles and choice not in env.targets:
                self.pos = choice

    def dijkstra(self,graph,initial):
        visited = {initial: 0}
        path = {}

        nodes = set(graph.nodes)
        while nodes: 
            min_node = None
            for node in nodes:
              if node in visited:
                if min_node is None:
                  min_node = node
                elif visited[node] < visited[min_node]:
                  min_node = node
            if min_node is None:
              break

            nodes.remove(min_node)
            current_weight = visited[min_node]

            for edge in graph.edges[min_node]:
                weight = current_weight + graph.distances[(min_node, edge)]
                if edge not in visited or weight < visited[edge]:
                    visited[edge] = weight
                    path[edge] = min_node
        return visited, path

    def shortest_path(self,graph, origin, destination):
        visited, paths = self.dijkstra(graph, origin)
        full_path = deque()
        _destination = paths[destination]

        while _destination != origin:
            full_path.appendleft(_destination)
            _destination = paths[_destination]

        full_path.appendleft(origin)
        full_path.append(destination)

        return visited[destination], list(full_path)