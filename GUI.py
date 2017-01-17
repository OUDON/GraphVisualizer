# coding: utf-8
import sys
from PyQt4 import QtGui, QtCore
from Graph import VisualizableGraph
from form import Ui_GraphVisualizer
from graph_view import GraphView

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_GraphVisualizer()
        self.ui.setupUi(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 500, 500)
        self.ui.graphicsView.setScene(self.scene)
        self.graphView = GraphView(500, 500)
        self.scene.addItem(self.graphView)

        self.ui.button_draw.clicked.connect(self.loadGraph)
        self.initGraphView()

    def initGraphView(self):
        self.graph = VisualizableGraph()
        self.graph.load_from_file('data/graph4.txt')
        self.graphView.setGraph(self.graph)

    def loadGraph(self):
        graph_str = self.ui.text_graph.toPlainText()
        directed  = self.ui.radiobtn_directed.isChecked()
        weighted  = self.ui.checkbox_weighted.isChecked()
        self.graph.load(graph_str, directed, weighted)
        self.graphView.setGraph(self.graph)

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
