# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.link_line_edit = QtWidgets.QLineEdit(self.widget)
        self.link_line_edit.setObjectName("link_line_edit")
        self.gridLayout.addWidget(self.link_line_edit, 3, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.format_line_edit = QtWidgets.QLineEdit(self.widget)
        self.format_line_edit.setObjectName("format_line_edit")
        self.gridLayout.addWidget(self.format_line_edit, 4, 1, 1, 1)
        self.start_at_line_edit = QtWidgets.QLineEdit(self.widget)
        self.start_at_line_edit.setObjectName("start_at_line_edit")
        self.gridLayout.addWidget(self.start_at_line_edit, 5, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.name_line_edit = QtWidgets.QLineEdit(self.widget)
        self.name_line_edit.setObjectName("name_line_edit")
        self.gridLayout.addWidget(self.name_line_edit, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.destination_line_edit = QtWidgets.QLineEdit(self.widget)
        self.destination_line_edit.setObjectName("destination_line_edit")
        self.gridLayout.addWidget(self.destination_line_edit, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.file_name_line_edit = QtWidgets.QLineEdit(self.widget)
        self.file_name_line_edit.setObjectName("file_name_line_edit")
        self.gridLayout.addWidget(self.file_name_line_edit, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.end_at_line_edit = QtWidgets.QLineEdit(self.widget)
        self.end_at_line_edit.setObjectName("end_at_line_edit")
        self.gridLayout.addWidget(self.end_at_line_edit, 6, 1, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_6.setText(_translate("Dialog", "Start at"))
        self.label_3.setText(_translate("Dialog", "File Name"))
        self.label_4.setText(_translate("Dialog", "Link"))
        self.label.setText(_translate("Dialog", "Name"))
        self.label_2.setText(_translate("Dialog", "Destination"))
        self.label_5.setText(_translate("Dialog", "Format"))
        self.label_7.setText(_translate("Dialog", "End at"))
