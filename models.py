from PyQt5 import QtCore, QtWidgets


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self.videos = data
        self.header = [
            '#',
            'Name',
            'Progress',
            'Status'
        ]

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.videos[index.row()][index.column()]

    def rowCount(self, index):
        return len(self.videos)

    def columnCount(self, index):
        return len(self.videos[0])

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.header[section]


class ProgressDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        progress = index.data()
        opt = QtWidgets.QStyleOptionProgressBar()
        opt.rect = option.rect
        opt.minimum = 0
        opt.maximum = 100
        opt.progress = progress
        opt.text = "{}%".format(progress)
        opt.textVisible = True
        QtWidgets.QApplication.style().drawControl(
            QtWidgets.QStyle.CE_ProgressBar, opt, painter)
