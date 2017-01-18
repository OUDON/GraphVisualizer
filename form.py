# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_GraphVisualizer(object):
    def setupUi(self, GraphVisualizer):
        GraphVisualizer.setObjectName(_fromUtf8("GraphVisualizer"))
        GraphVisualizer.resize(680, 524)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(GraphVisualizer)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.text_graph = QtGui.QTextEdit(GraphVisualizer)
        self.text_graph.setObjectName(_fromUtf8("text_graph"))
        self.verticalLayout.addWidget(self.text_graph)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radiobtn_undirected = QtGui.QRadioButton(GraphVisualizer)
        self.radiobtn_undirected.setChecked(True)
        self.radiobtn_undirected.setObjectName(_fromUtf8("radiobtn_undirected"))
        self.horizontalLayout.addWidget(self.radiobtn_undirected)
        self.radiobtn_directed = QtGui.QRadioButton(GraphVisualizer)
        self.radiobtn_directed.setObjectName(_fromUtf8("radiobtn_directed"))
        self.horizontalLayout.addWidget(self.radiobtn_directed)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.checkbox_weighted = QtGui.QCheckBox(GraphVisualizer)
        self.checkbox_weighted.setObjectName(_fromUtf8("checkbox_weighted"))
        self.verticalLayout.addWidget(self.checkbox_weighted)
        self.button_draw = QtGui.QPushButton(GraphVisualizer)
        self.button_draw.setObjectName(_fromUtf8("button_draw"))
        self.verticalLayout.addWidget(self.button_draw)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.graphicsView = QtGui.QGraphicsView(GraphVisualizer)
        self.graphicsView.setMinimumSize(QtCore.QSize(500, 500))
        self.graphicsView.setResizeAnchor(QtGui.QGraphicsView.NoAnchor)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout_2.addWidget(self.graphicsView)

        self.retranslateUi(GraphVisualizer)
        QtCore.QMetaObject.connectSlotsByName(GraphVisualizer)

    def retranslateUi(self, GraphVisualizer):
        GraphVisualizer.setWindowTitle(_translate("GraphVisualizer", "GraphVisualizer", None))
        self.text_graph.setHtml(_translate("GraphVisualizer", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">13 16</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">1 2</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">3 1</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">2 3</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">7 3</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">7 5</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">1 6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">4 6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">6 5</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">5 4</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">8 9</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">8 7</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">7 10</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">10 11</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">10 12</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">12 13</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">10 13</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.radiobtn_undirected.setText(_translate("GraphVisualizer", "無向", None))
        self.radiobtn_directed.setText(_translate("GraphVisualizer", "有向", None))
        self.checkbox_weighted.setText(_translate("GraphVisualizer", "重み付き", None))
        self.button_draw.setText(_translate("GraphVisualizer", "描画", None))

