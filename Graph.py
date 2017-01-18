# coding: utf-8
import numpy as np
import math
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore

import argparse
import sys

COULOMB_CONSTANT    = 50.0
SPRING_CONSTANT     = 1.0
NATURAL_LENGTH_MAX  = 50
TIME_STEP           = 0.5 
DAMPING_COEFFICIENT = 0.8

class Edge:
    def __init__(self, frm, to, weight, edge_type):
        self.frm               = frm
        self.to                = to
        self.weight            = weight
        self.normalized_weight = 1
        self.edge_type         = edge_type

    def weight_normalize(self, max_weight):
        self.normalized_weight = self.weight / max_weight

class Graph(object):    
    def __init__(self):
        self.N, self.M = 0, 0
        self.weighted  = False
        self.directed  = False
        self.graph     = []
    
    def load(self, graph_str, directed=False, weighted=False):
        graph_str = graph_str.rstrip().split('\n')
        splitted_line = graph_str[0].split(' ')
        self.N, self.M = int(splitted_line[0]), int(splitted_line[1])
        self.graph = [[] for i in range(self.N)]

        self.directed = directed
        self.weighted = weighted

        for line in graph_str[1:]:
            splitted_line = line.split(' ')
            u, v = int(splitted_line[0]) - 1, int(splitted_line[1]) - 1
            weight = int(splitted_line[2]) if weighted else 1

            if self.directed:
                self.graph[u].append(Edge(u, v, weight, 'directed'))
                self.graph[v].append(Edge(v, u, weight, 'directed-inverse'))
            else:
                self.graph[u].append(Edge(u, v, weight, 'undirected'))
                self.graph[v].append(Edge(v, u, weight, 'undirected'))
        if weighted: self.__weight_normalize()

    def load_from_file(self, file_name, directed=False, weighted=False):
        with open(file_name) as f:
            graph_str = f.read()
            self.load(graph_str, directed, weighted)

    def dump(self):
        for u in range(self.N):
            print("{}: ".format(u+1), end='')
            for edge in self.graph[u]:
                if edge.edge_type == 'directed-inverse': continue
                print("{} ".format(edge.to+1), end='')
            print("")

    def __weight_normalize(self):
        max_weight = 0
        for u in range(self.N):
            for edge in self.graph[u]:
                max_weight = max(max_weight, edge.weight)
        for u in range(self.N):
            for edge in self.graph[u]:
                edge.weight_normalize(max_weight)

class VisualizableGraph(QtGui.QGraphicsItem, Graph):
    def __init__(self, width=500, height=500, mergin=50):
        super(VisualizableGraph, self).__init__()
        Graph.__init__(self)

        self.pos = []
        self.width = width
        self.height = height
        self.mergin = mergin

    def load(self, graph_str, directed=False, weighted=False):
        Graph.load(self, graph_str, directed, weighted)
        self.compute_node_position()
        self.resize_graph()
        self.update()

    def resize_graph(self):
        w = self.width - self.mergin*2
        h = self.height - self.mergin*2
        self.__position_normalize(w, h, self.mergin)

    def __position_normalize(self, width, height, mergin):
        x_range = np.amax(self.pos.T[0]) - np.amin(self.pos.T[0])
        x_min   = np.amin(self.pos.T[0])
        y_range = np.amax(self.pos.T[1]) - np.amin(self.pos.T[1])
        y_min   = np.amin(self.pos.T[1])

        for i in range(self.N):
            self.pos[i][0] = (self.pos[i][0] - x_min) * width / x_range + mergin
            self.pos[i][1] = (self.pos[i][1] - y_min) * height / y_range + mergin

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
            springLengthX = NATURAL_LENGTH_MAX * edge.normalized_weight * dx / l
            springLengthY = NATURAL_LENGTH_MAX * edge.normalized_weight * dy / l

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

    # Methods for QtGui.QGraphicsItem
    def paint(self, painter, option, widget):
        self.__draw_graph(painter)

    def __draw_graph(self, painter):
        G = self.graph
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.white)

        for u in range(self.N):
          for edge in G[u]:
              self.__draw_edge(edge, painter)

        #"""
        # node
        for u in range(self.N):
            x, y = self.pos[u][0], self.pos[u][1]
            painter.drawEllipse(QtCore.QPointF(x, y), 20, 20)

        # label
        painter.setFont(QtGui.QFont('Helvetica', 24))
        for u in range(self.N):
            x, y = self.pos[u][0], self.pos[u][1]
            painter.drawText(x-20, y-20, 40, 40, QtCore.Qt.AlignCenter, str(u+1))
        #"""

    def __draw_edge(self, edge, painter):
        u, v = edge.frm, edge.to
        # f, t = self.pos[u], self.pos[v]
        tmp_f, tmp_t = self.pos[u], self.pos[v]
        direction = (tmp_t - tmp_f) / np.linalg.norm(tmp_t - tmp_f)
        f = tmp_f + direction * 20
        t = tmp_t - direction * 20

        dx = (t - f)[0]
        dy = (t - f)[1]
        length = np.linalg.norm(t - f)

        if edge.edge_type == 'undirected':
            painter.drawLine(f[0], f[1], t[0], t[1])

        elif edge.edge_type == 'directed':
            angle = math.acos(dx / length)
            if dy >= 0:
                angle = 2 * math.pi - angle
            v1 = t + np.array([
                math.sin(angle - math.pi / 3) * 15,
                math.cos(angle - math.pi / 3) * 15
            ])

            v2 = t + np.array([
                math.sin(angle - math.pi * 2 / 3) * 15,
                math.cos(angle - math.pi * 2 / 3) * 15
            ])

            painter.drawLine(f[0], f[1], t[0], t[1])
            painter.drawLine(v1[0], v1[1], t[0], t[1])
            painter.drawLine(v2[0], v2[1], t[0], t[1])

        elif edge.edge_type == 'directed-inverse':
            pass

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width, self.height)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--directed', action='store_true')
    parser.add_argument('--weighted', action='store_true')
    args = parser.parse_args()

    with open(args.file_name) as f:
        graph_str = f.read()
    graph_str = graph_str.rstrip()

    G = VisualizableGraph()
    G.load(graph_str, args.directed, args.weighted)
    G.dump()
    G.show()
