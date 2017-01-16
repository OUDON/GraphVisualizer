# coding: utf-8
import sys
from PyQt4 import QtGui, QtCore
from Graph import VisualizableGraph

class GraphView(QtGui.QGraphicsItem):
    def __init__(self, width=500, height=500, size=5):
        super(GraphView, self).__init__()

        self.width  = width
        self.height = height
        self.size   = size
        self.mergin = 50

        self.graph = VisualizableGraph()
        self.graph.load_from_file('data/graph4.txt')
        self.resizeGraph()

    def resizeGraph(self):
        w = self.width - self.mergin*2
        h = self.height - self.mergin*2
        self.graph.position_normalize(w, h, self.mergin)

    def loadGraph(self, graph_str, directed=False, weighted=False):
        self.graph.load(graph_str, directed, weighted)
        self.resizeGraph()
        self.update()

    def paint(self, painter, option, widget):
        self.drawGraph(painter)

    def drawGraph(self, qp):
        G = self.graph.graph
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.white)

        # edge
        for u in range(self.graph.N):
          for edge in G[u]:
              v = edge.to
              f, t = self.graph.pos[u], self.graph.pos[v]
              qp.drawLine(f[0], f[1], t[0], t[1])

        # node
        for u in range(self.graph.N):
            x, y = self.graph.pos[u][0], self.graph.pos[u][1]
            qp.drawEllipse(x-20, y-20, 40, 40)

        # label
        qp.setFont(QtGui.QFont('Helvetica', 24))
        for u in range(self.graph.N):
            x, y = self.graph.pos[u][0], self.graph.pos[u][1]
            qp.drawText(x-20, y-20, 40, 40, QtCore.Qt.AlignCenter, str(u+1))

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width, self.height)
