import os
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
from graph import Graph
from collections import deque


cmap = colors.ListedColormap(['black','white','yellow','green','red'])
bounds = [-2,1,0,1,2,3,4]
norm = colors.BoundaryNorm(bounds, cmap.N)

class Environment:
    def __init__(self):
        self.num_rows = self.num_cols = 16
        self.map = np.zeros((self.num_rows, self.num_cols))
        self.state_size = self.num_rows * self.num_cols
        self.num_obstacles = int((self.num_rows * self.num_cols) * .2)

        self.targets = [
            (0,0),
            (0,self.num_cols-1),
            (self.num_rows-1,0),
            (self.num_rows-1, self.num_cols-1)
        ]

    def set_env(self):
        self.map = np.zeros((self.num_rows, self.num_cols))
        self.obstacles = []

        while len(self.obstacles) < self.num_obstacles:
            choice = (random.randint(0,self.num_rows-1), random.randint(0,self.num_cols-1))
            if choice not in self.obstacles \
                and choice not in self.targets \
                and np.all(np.abs(np.subtract(self.goal,choice)) != 1):
                self.obstacles.append(choice)

        for t in self.targets:
            if t == self.goal:
                self.map[t[0],t[1]] = 3
            else:
                self.map[t[0],t[1]] = 2
        for t in self.obstacles:
            self.map[t[0],t[1]] = 1

    def register_agent(self, agent):
        x,y = agent.pos
        self.map[x,y] = 3
        self.convert_to_graph()

    def update_env(self,pos_t0,pos_t1):
        r,c = pos_t0
        if pos_t0 == self.goal:
            self.map[r,c] = 2
        elif pos_t0 in self.targets:
            self.map[r,c] = 1
        elif pos_t0 in self.obstacles:
            self.map[r,c] = -1
        else:
            self.map[r,c] = 0
        r,c = pos_t1
        self.map[r,c] = 3

    def convert_to_graph(self):
        self.graph = Graph()
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                node = (r,c)
                if node not in self.obstacles:
                    self.graph.add_node(node)
        self.graph.add_node(self.goal)
        for node1 in self.graph.nodes:
            for node2 in self.graph.nodes:
                if np.abs(node1[0]-node2[0]) <2 and np.abs(node1[1]-node2[1])<2 and node1!=node2:
                    self.graph.add_edge(node1, node2,1)

    def plot_map(self):
        plt.imshow(self.map,interpolation='nearest',cmap=cmap, norm=norm)
        plt.xticks([x -.5 for x in range(self.num_rows)],[x for x in range(self.num_rows)])
        plt.yticks([x -.5 for x in range(self.num_rows)],[x for x in range(self.num_rows)])
        plt.grid(1)
        plt.show()

    def save_map(self):
        # print(str(len(os.listdir('maps'))).zfill(3))
        # print(env.map)
        plt.imshow(self.map,interpolation='nearest',cmap=cmap, norm=norm)
        plt.xticks([x -.5 for x in range(self.num_rows)],[x for x in range(self.num_rows)])
        plt.yticks([x -.5 for x in range(self.num_rows)],[x for x in range(self.num_rows)])
        plt.grid(1)
        plt.savefig("maps/map_%s.png" % (str(len(os.listdir('maps'))).zfill(3)))
