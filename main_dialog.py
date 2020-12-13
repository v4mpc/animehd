from PyQt5 import QtWidgets
from dialog import Ui_Dialog
from PyQt5.QtCore import QObject, pyqtSignal


class DialogSignal(QObject):
    data = pyqtSignal(dict)


class AddDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.signals = DialogSignal()

    def accept(self):
        if True:
            print('dialog Accepted')
            self.signals.data.emit({
                'name': self.ui.name_line_edit.text(),
                'destination': self.ui.destination_line_edit.text(),
                'file_name': self.ui.file_name_line_edit.text(),
                'link': self.ui.link_line_edit.text(),
                'format': self.ui.format_line_edit.text(),
                'start_at': self.ui.start_at_line_edit.text(),
                'end_at': self.ui.end_at_line_edit.text()
            })
            self.done(QtWidgets.QDialog.Accepted)
