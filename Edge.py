# coding: utf-8
import numpy as np
import math
from PyQt4 import QtGui, QtCore

class Edge:
    def __init__(self, args):
        self.frm               = args['frm']
        self.to                = args['to']
        self.edge_type         = args['edge_type']
        self.weight            = args.get('weight', 1)
        self.weighted          = args.get('weighted', False)
        self.node_pos_frm      = args.get('pos_frm', None)
        self.node_pos_to       = args.get('pos_to', None)
        self.color             = args.get('color', QtCore.Qt.black)
        self.normalized_weight = 1

    def update_edge_pos(self, pos_frm, pos_to, node_radius=20):
        self.node_pos_frm = pos_frm
        self.node_pos_to  = pos_to
        self._adjust(node_radius)

    def _adjust(self, node_radius=20):
        vec = self.node_pos_to - self.node_pos_frm
        direction = vec / np.linalg.norm(vec)
        self.pos_frm = self.node_pos_frm + direction * 20
        self.pos_to  = self.node_pos_to - direction * 20

    def weight_normalize(self, max_weight):
        self.normalized_weight = self.weight / max_weight

    def make_edge_type(directed=False, inverse=False):
        if directed:
            edge_type = 'directed' if not inverse else 'directed-inverse'
        else:
            edge_type = 'undirected'
        return edge_type

    def is_forward(self):
        return self.edge_type != 'directed-inverse'

    def dx(self):
        return (self.pos_to - self.pos_frm)[0]

    def dy(self):
        return (self.pos_to - self.pos_frm)[1]

    def length(self):
        return np.linalg.norm(self.pos_to - self.pos_frm)

    def direction(self):
        return (self.pos_to - self.pos_frm) / self.length()

    # Methods for draw
    def draw(self, painter):
        if not self.is_forward(): return 

        u, v = self.frm, self.to
        direction = self.direction()
        f, t = self.pos_frm, self.pos_to

        painter.setPen(self.color)
        painter.drawLine(f[0], f[1], t[0], t[1])
        if self.weighted:
            center = f + self.direction() * self.length() / 2

            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(center[0]-10, center[1]-10, 20, 20)

            painter.setPen(QtCore.Qt.black)
            painter.setFont(QtGui.QFont('Helvetica', 16))
            painter.drawText(center[0]-40, center[1]-20, 80, 40, QtCore.Qt.AlignCenter, str(self.weight))

        if self.edge_type == 'directed':
            angle = math.acos(self.dx() / self.length())
            if self.dy() >= 0:
                angle = 2 * math.pi - angle
            v1 = t + np.array([
                math.sin(angle - math.pi / 3) * 15,
                math.cos(angle - math.pi / 3) * 15
            ])

            v2 = t + np.array([
                math.sin(angle - math.pi * 2 / 3) * 15,
                math.cos(angle - math.pi * 2 / 3) * 15
            ])

            painter.setPen(self.color)
            painter.drawLine(v1[0], v1[1], t[0], t[1])
            painter.drawLine(v2[0], v2[1], t[0], t[1])

    def set_color(self, color):
        self.color = color

class Edges(dict):
    def __init__(self, input={}):
        super(Edges, self).__init__(input)

    def __getattr__(self, node_pair):
        self._sort_node_pair(node_pair)
        return self.__getattr__(self, node_pair);

    def __setattr__(self, node_pair, value):
        self._sort_node_pair(node_pair)
        pass

    def _sort_node_pair(self, node_pair):
        if node_pair[0] > node_pair[1]:
            node_pair[0], node_pair[1] = node_pair[1], node_pair[0]
