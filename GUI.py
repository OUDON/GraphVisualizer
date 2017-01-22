# coding: utf-8
import sys
import functools
from PyQt4 import QtGui, QtCore
from Graph import VisualizableGraph

from ui import mainwindow
from ui import shortest_path_dialog

class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)
        self.move(200, 50)
        self.initMenuBar()
        self.shortest_path_dialog = ShortestPathDialog(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 500, 500)
        self.graphicsView.setScene(self.scene)

        self.graph = VisualizableGraph()
        self.scene.addItem(self.graph)

        self.button_draw.clicked.connect(self.loadGraph)
        self.initGraph()

    def initMenuBar(self):
        self.actionShortestPath.triggered.connect(self.open_shortest_path_dialog)
        self.actionMST.triggered.connect(self.mst)
        self.actionReset.triggered.connect(self.reset_algorithm_result)

    def initGraph(self):
        self.graph.load_from_file('data/graph4.txt')

    def loadGraph(self):
        graph_str = self.text_graph.toPlainText()
        directed  = self.radiobtn_directed.isChecked()
        weighted  = self.checkbox_weighted.isChecked()
        indexed   = int(self.radiobtn_indexed_1.isChecked())
        self.graph.load(graph_str, directed, weighted, indexed)

    def open_shortest_path_dialog(self):
        self.shortest_path_dialog.show()

    def shortest_path(self, idx_from, idx_to):
        self.graph.shortest_path(idx_from, idx_to)

    def mst(self):
        self.graph.mst()

    def reset_algorithm_result(self):
        self.graph.reset_algorithm_result()

class ShortestPathDialog(QtGui.QDialog, shortest_path_dialog.Ui_ShortestPathDialog):
    def __init__(self, parent=None):
        super(ShortestPathDialog, self).__init__(parent)
        self.setupUi(self)
        self.move(200, 350)
        self.parent = parent
        self.button_exec.clicked.connect(self.button_exec_clicked)

    def button_exec_clicked(self):
        self.parent.shortest_path(self._idx_from(), self._idx_to())

    def _idx_from(self):
        return int(self.input_from.text())

    def _idx_to(self):
        return int(self.input_to.text())

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
