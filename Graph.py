# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt

import argparse
import sys

COULOMB_CONSTANT    = 50.0
SPRING_CONSTANT     = 1.0
NATURAL_LENGTH_MAX  = 50
TIME_STEP           = 0.5 
DAMPING_COEFFICIENT = 0.8

class Edge:
    def __init__(self, to, weight):
        self.to = to
        self.weight = weight

class Graph:
    def __init__(self, file_name, weighted=False):
        self.__load(file_name, weighted)
        if weighted:
            self.__weight_normalize()
    
    def dump(self):
        for u in range(self.N):
            print("{}: ".format(u+1), end='')
            for edge in self.graph[u]:
                print("{} ".format(edge.to+1), end='')
            print("")

    def __weight_normalize(self):
        max_weight = 0
        for u in range(self.N):
            for edge in self.graph[u]:
                max_weight = max(max_weight, edge.weight)
        for u in range(self.N):
            for edge in self.graph[u]:
                edge.weight /= max_weight

    def __load(self, file_name, weighted=False):
        with open(file_name, 'r') as f:
            splitted_line = f.readline().split(' ')
            self.N, self.M = int(splitted_line[0]), int(splitted_line[1])
            self.graph = [[] for i in range(self.N)]

            for line in f:
                splitted_line = line.split(' ')
                u, v = int(splitted_line[0]) - 1, int(splitted_line[1]) - 1
                weight = int(splitted_line[2]) if weighted else 1
                self.graph[u].append(Edge(v, weight))
                self.graph[v].append(Edge(u, weight))

class VisualizableGraph(Graph):
    def __init__(self, file_name, weighted=False):
        Graph.__init__(self, file_name, weighted)
        self.compute_node_position()

    def show(self):
        plt.plot(self.pos.T[0], self.pos.T[1], 'o')
        for u in range(len(self.graph)):
            for edge in self.graph[u]:
                v = edge.to
                plt.plot([self.pos[u][0], self.pos[v][0]],
                         [self.pos[u][1], self.pos[v][1]])
        plt.show()

    def compute_node_position(self):
        vs = np.zeros([self.N, 2])
        self.pos = np.random.randint(-300, 300, size=(self.N, 2)) * 1.0
        cnt = 1
        while True:
            cnt += 1
            E = 0.0
            for u in range(self.N):
                F = np.zeros(2)
                F += self.__compute_coulomb_force(u)
                F += self.__compute_spring_force(u)
                vs[u] = (vs[u] + TIME_STEP * F / 1.0) * DAMPING_COEFFICIENT
                self.pos[u] += TIME_STEP * vs[u] +  (F / 1.0) * TIME_STEP ** 2 / 2.0
                E += 1.0 * np.linalg.norm(vs[u]) ** 2 
            self.__centering(self.pos.T[0], self.pos.T[1])
            if E < 0.1 or cnt > 10000: break

    def __compute_coulomb_force(self, u):
        F = np.zeros(2)
        for v in range(self.N):
            if u == v: continue

            dx = self.pos[u][0] - self.pos[v][0]
            dy = self.pos[u][1] - self.pos[v][1]
            rSquared = dx * dx + dy * dy + 1e-5

            coulombForceX = COULOMB_CONSTANT * dx / rSquared
            coulombForceY = COULOMB_CONSTANT * dy / rSquared
            F[0] += coulombForceX
            F[1] += coulombForceY
        return F

    def __compute_spring_force(self, u):
        F = np.zeros(2)
        for edge in self.graph[u]:
            v = edge.to
            dx = self.pos[v][0] - self.pos[u][0]
            dy = self.pos[v][1] - self.pos[u][1]

            l = np.sqrt(dx * dx + dy * dy) + 1e-5
            springLengthX = NATURAL_LENGTH_MAX * edge.weight * dx / l
            springLengthY = NATURAL_LENGTH_MAX * edge.weight * dy / l

            F[0] += SPRING_CONSTANT * (dx - springLengthX)
            F[1] += SPRING_CONSTANT * (dy - springLengthY)
        return F

    def __centering(self, xs, ys):
        gx, gy = 0.0, 0.0
        for i in range(self.N):
            gx += self.pos[i][0] / self.N
            gy += self.pos[i][1] / self.N
        for i in range(self.N):
            self.pos[i][0] -= gx
            self.pos[i][1] -= gy

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--weighted', action='store_true')
    args = parser.parse_args()

    G = VisualizableGraph(args.file_name, args.weighted)
    G.dump()
    G.show()
