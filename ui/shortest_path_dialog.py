# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shortest_path_dialog.ui'
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

class Ui_ShortestPathDialog(object):
    def setupUi(self, ShortestPathDialog):
        ShortestPathDialog.setObjectName(_fromUtf8("ShortestPathDialog"))
        ShortestPathDialog.resize(231, 130)
        self.verticalLayout = QtGui.QVBoxLayout(ShortestPathDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(ShortestPathDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.input_from = QtGui.QLineEdit(ShortestPathDialog)
        self.input_from.setObjectName(_fromUtf8("input_from"))
        self.horizontalLayout.addWidget(self.input_from)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(ShortestPathDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.input_to = QtGui.QLineEdit(ShortestPathDialog)
        self.input_to.setObjectName(_fromUtf8("input_to"))
        self.horizontalLayout_2.addWidget(self.input_to)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.button_exec = QtGui.QPushButton(ShortestPathDialog)
        self.button_exec.setObjectName(_fromUtf8("button_exec"))
        self.verticalLayout.addWidget(self.button_exec)

        self.retranslateUi(ShortestPathDialog)
        QtCore.QMetaObject.connectSlotsByName(ShortestPathDialog)

    def retranslateUi(self, ShortestPathDialog):
        ShortestPathDialog.setWindowTitle(_translate("ShortestPathDialog", "Shortest Path", None))
        self.label.setText(_translate("ShortestPathDialog", "始点 :", None))
        self.label_2.setText(_translate("ShortestPathDialog", "終点 :", None))
        self.button_exec.setText(_translate("ShortestPathDialog", "実行", None))

