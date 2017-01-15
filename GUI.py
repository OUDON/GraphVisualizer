# coding: utf-8
import sys
from PyQt4 import QtGui, QtCore
from Graph import VisualizableGraph

class GraphVisualizer(QtGui.QWidget):
    def __init__(self):
        super(GraphVisualizer, self).__init__()

        width, height = 400, 400
        mergin = 50

        self.initUI(width+2*mergin, height+2*mergin)
        self.graph = VisualizableGraph('data/graph4.txt')
        self.graph.position_normalize(width, height, 50)

    def initUI(self, width, height):
        self.setGeometry(100, 100, width, height)
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawGraph(qp)
        qp.end()

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

def main():
    app = QtGui.QApplication(sys.argv)
    ex = GraphVisualizer()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
