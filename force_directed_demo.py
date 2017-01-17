# coding: utf-8
import random
import numpy as np
import matplotlib.pyplot as plt
from Graph import Graph
import sys

COULOMB_CONSTANT    = 50.0
SPRING_CONSTANT     = 1.0
TIME_STEP           = 0.5 
DAMPING_COEFFICIENT = 0.8

def show_graph(graph, pos_x, pos_y):
    plt.plot(pos_x, pos_y, 'o')
    for u in range(len(graph)):
        for v in graph[u]:
            plt.plot([pos_x[u], pos_x[v]], [pos_y[u], pos_y[v]])
    plt.show()


class RealTimePlot:
    def __init__(self, x, y, graph):
        self.fig, self.ax = plt.subplots(1, 1)
        self.lines, = self.ax.plot(x, y, 'o')
        self.energy_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes)

        self.ax.set_xlim((-250, 250))
        self.ax.set_ylim((-250, 250))
        plt.pause(0.00001)

    def update(self, x, y):
        self.lines.set_data(x, y)
        plt.pause(0.00001)

    def set_energy_text(self, E):
        self.energy_text.set_text('E = {0:.3f}'.format(E))


class Animation:
    def __init__():
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, aspect='equal', autoscale_on=False,
                                       xlim=(-300, 300), ylim=(-300, 300))
        self.ax.grid()
        self.line, = self.set_data([], [])
        time_text.set_text('')

    def animate(i):
        line.set_data(x, y)


def centering(xs, ys):
    gx, gy = 0.0, 0.0
    n = len(xs)
    for i in range(n):
        gx += xs[i] / n
        gy += ys[i] / n
    for i in range(n):
        xs[i] -= gx
        ys[i] -= gy


def compute_node_position(graph):
    n = len(graph)
    vs = np.zeros([n, 2]);
    pos = np.random.randint(-300, 300, size=(n, 2)) * 1.0
    rplt = RealTimePlot(pos.T[0], pos.T[1], graph)

    cnt = 1
    while True:
        # print("---------------")
        # print("Iteration {}:".format(cnt))
        cnt += 1

        E = 0.0
        for u in range(n):
            F = np.zeros(2)

            # """
            # クーロン力による力
            for v in range(n):
                if u == v: continue

                dx = pos[u][0] - pos[v][0]
                dy = pos[u][1] - pos[v][1]
                rSquared = dx * dx + dy * dy + 1e-5

                coulombForceX = COULOMB_CONSTANT * dx / rSquared
                coulombForceY = COULOMB_CONSTANT * dy / rSquared

                F[0] += coulombForceX
                F[1] += coulombForceY

                # diff = pos[u] - pos[v]
                # dist = np.linalg.norm(diff) + 1e-10
                # F += COULOMB_CONSTANT * diff / (dist ** 3)
            # """

            # """
            # フックの法則による力
            for v in graph[u]:
                dx = pos[v][0] - pos[u][0]
                dy = pos[v][1] - pos[u][1]

                l = np.sqrt(dx * dx + dy * dy) + 1e-5
                springLengthX = 50 * dx / l
                springLengthY = 50 * dy / l

                F[0] += SPRING_CONSTANT * (dx - springLengthX)
                F[1] += SPRING_CONSTANT * (dy - springLengthY)

                # dist = np.linalg.norm(pos[u] - pos[v]) + 1e-10
                # diff = pos[u] - pos[v]
                # F += -SPRING_CONSTANT * (diff - 1.0) * diff / dist
            # """

            vs[u] = (vs[u] + TIME_STEP * F / 1.0) * DAMPING_COEFFICIENT
            pos[u] += TIME_STEP * vs[u] +  (F / 1.0) * TIME_STEP ** 2 / 2.0
            # pos[u] += TIME_STEP * vs[u] # +  (F / 1.0) * TIME_STEP ** 2 / 2.0

            E += 1.0 * np.linalg.norm(vs[u]) ** 2 
            # print("  F = {}".format(F))

        centering(pos.T[0], pos.T[1])
        rplt.set_energy_text(E)
        rplt.update(pos.T[0], pos.T[1])
        if E < 0.1 or cnt > 10000: break

    print("End")
    print("  E = {}".format(E))
    show_graph(graph, pos.T[0], pos.T[1])


def main():
    G = Graph()
    # G.load('data/graph3.txt')
    G.load(sys.argv[1])
    G.dump()
    compute_node_position(G.graph)


if __name__ == "__main__":
    main()
