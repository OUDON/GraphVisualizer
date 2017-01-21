# coding: utf-8
import sys
from PyQt4 import QtGui, QtCore
from Graph import VisualizableGraph
import mainwindow

class MainWindow(QtGui.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 500, 500)
        self.graphicsView.setScene(self.scene)

        self.graph = VisualizableGraph()
        self.scene.addItem(self.graph)

        self.button_draw.clicked.connect(self.loadGraph)
        self.initGraph()

    def initGraph(self):
        self.graph.load_from_file('data/graph4.txt')

    def loadGraph(self):
        graph_str = self.text_graph.toPlainText()
        directed  = self.radiobtn_directed.isChecked()
        weighted  = self.checkbox_weighted.isChecked()
        self.graph.load(graph_str, directed, weighted)

def main():
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
