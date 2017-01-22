# coding: utf-8
import numpy as np
import math
import matplotlib.pyplot as plt
from PyQt4 import QtGui, QtCore
from Edge import Edge, Edges

import argparse
import sys

from UnionFind import UnionFind
import heapq

COULOMB_CONSTANT    = 50.0
SPRING_CONSTANT     = 1.0
NATURAL_LENGTH_MAX  = 50
TIME_STEP           = 0.5 
DAMPING_COEFFICIENT = 0.8

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
                self.graph[u].append(self._make_edge(u, v, weight))
                self.graph[v].append(self._make_edge(v, u, weight, inverse=True))
            else:
                self.graph[u].append(self._make_edge(u, v, weight))
                self.graph[v].append(self._make_edge(v, u, weight))
        if weighted: self.__weight_normalize()

    def _make_edge(self, frm, to, weight, inverse=False):
        edge = Edge({
             'frm':       frm,
             'to':        to,
             'weight':    weight,
             'weighted':   self.is_weighted(),
             'edge_type': Edge.make_edge_type(self.directed, inverse),
        })
        return edge

    def load_from_file(self, file_name, directed=False, weighted=False):
        with open(file_name) as f:
            graph_str = f.read()
            self.load(graph_str, directed, weighted)

    def is_weighted(self):
        return self.weighted

    def is_directed(self):
        return self.directed

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

    def shortest_path(self, s, t):
        dist = [float('inf')] * self.N
        prev = [-1] * self.N
        Q = []
        dist[s] = 0
        heapq.heappush(Q, (0, s))

        while len(Q):
            p = heapq.heappop(Q)
            if p[0] > dist[p[1]]: continue
            v = p[1]

            for edge in self.graph[v]:
                if edge.is_forward() and dist[edge.to] > dist[v] + edge.weight:
                    dist[edge.to] = dist[v] + edge.weight
                    prev[edge.to] = v
                    heapq.heappush(Q, (dist[edge.to], edge.to))

        path = []
        u = t
        while u != -1:
            path.append(u)
            u = prev[u]
        path.reverse()
        return dist[t], path

    def mst(self):
        union_find = UnionFind(self.N)

        edges = []
        for u in range(self.N):
            for edge in self.graph[u]:
                if u <= edge.to: continue
                edges.append((u, edge.to, edge.weight))
        edges.sort(key=lambda x:x[2])

        weight_sum = 0
        mst_edges  = []
        for edge in edges:
            if not union_find.is_same(edge[0], edge[1]):
                union_find.merge(edge[0], edge[1])
                mst_edges.append(edge)
                weight_sum += edge[2]
        return weight_sum, mst_edges

class VisualizableGraph(QtGui.QGraphicsItem, Graph):
    def __init__(self, width=500, height=500, mergin=50):
        super(VisualizableGraph, self).__init__()
        Graph.__init__(self)

        self.pos               = []
        self.width             = width
        self.height            = height
        self.mergin            = mergin
        self.__init_paint()

        self.highlighted_edges = []
        self.algorithm_result  = None

        self.node_radius = 20

    def load(self, graph_str, directed=False, weighted=False):
        Graph.load(self, graph_str, directed, weighted)
        self.compute_node_position()
        self.resize_graph()
        self.update_edge_pos()
        self._reset_algorithm_result()
        self.update()

    def _make_edge(self, frm, to, weight, inverse=False, highlight=False):
        color = QtCore.Qt.red if highlight else QtCore.Qt.black
        edge = Edge({
             'frm':       frm,
             'to':        to,
             'weight':    weight,
             'weighted':  self.is_weighted(),
             'color':     color,
             'edge_type': Edge.make_edge_type(self.directed, inverse),
        })
        return edge

    def resize_graph(self):
        w = self.width - self.mergin*2
        h = self.height - self.mergin*2
        self.__position_normalize(w, h, self.mergin)

    def update_edge_pos(self):
        for u in range(self.N):
            for edge in self.graph[u]:
                edge.update_edge_pos(self.pos[u], self.pos[edge.to], self.node_radius)

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

    # Graph Algorithms
    def _reset_algorithm_result(self):
        self.algorithm_result  = None
        self.highlighted_edges = []

    def shortest_path(self, s, t):
        dist, path = Graph.shortest_path(self, s, t)
        self._reset_algorithm_result()
        self.algorithm_result = "最短経路長: {}".format(dist)

        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]

            for edge in self.graph[u]:
                if edge.to == v:
                    weight = edge.weight
                    break

            edge = self._make_edge(u, v, weight, highlight=True)
            edge.update_edge_pos(self.pos[u], self.pos[v], self.node_radius)
            self.highlighted_edges.append(edge)
        self.update()

    def mst(self):
        weight_sum, edges = Graph.mst(self)
        self._reset_algorithm_result()
        self.algorithm_result = "最小全域木コスト: {}".format(weight_sum)

        for e in edges:
            edge = self._make_edge(e[0], e[1], e[2], highlight=True)
            edge.update_edge_pos(self.pos[e[0]], self.pos[e[1]], self.node_radius)
            self.highlighted_edges.append(edge)
        self.update()

    # Methods for QtGui.QGraphicsItem
    def __init_paint(self):
        self.__pen_black = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        self.__pen_red   = QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.SolidLine)
        self.__no_pen    = QtCore.Qt.NoPen

    def paint(self, painter, option, widget):
        self.__draw_graph(painter)

    def __draw_graph(self, painter):
        G = self.graph
        painter.setPen(self.__pen_black)
        painter.setBrush(QtCore.Qt.white)

        self.__draw_edges(painter)
        for edge in self.highlighted_edges:
            edge.draw(painter)

        # node
        painter.setPen(QtCore.Qt.black)
        for u in range(self.N):
            x, y = self.pos[u][0], self.pos[u][1]
            painter.drawEllipse(QtCore.QPointF(x, y), 20, 20)

        # label
        painter.setFont(QtGui.QFont('Helvetica', 24))
        for u in range(self.N):
            x, y = self.pos[u][0], self.pos[u][1]
            painter.drawText(x-20, y-20, 40, 40, QtCore.Qt.AlignCenter, str(u+1))

        if self.algorithm_result != None:
            painter.setFont(QtGui.QFont('Helvetica', 20))
            painter.drawText(10, 0, 500, 20, QtCore.Qt.AlignTop, self.algorithm_result)

    def __draw_edges(self, painter):
        for u in range(self.N):
          for edge in self.graph[u]:
              edge.draw(painter)
        
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
