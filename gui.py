from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QObject, QRunnable, QThreadPool, QTimer, pyqtSignal, pyqtSlot
from MainWindow import Ui_MainWindow
import sys
import json
import time


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


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self.header = [
            '#',
            'Name',
            'Progress',
            'Status'
        ]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            # return self.header[]
            print(section)


class WorkerSignals(QObject):
    progress = pyqtSignal(int)


class Worker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.is_killed = False
        self.is_paused = False
        self.progress = 0

    @pyqtSlot()
    def run(self):
        try:
            self.progress += 10
            self.signals.progress.emit(self.progress)
            time.sleep(2)
            if self.is_killed:
                raise WorkerKilledException
        except WorkerKilledException:
            pass

    def kill(self):
        self.is_killed = True


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.delegate = ProgressDelegate(self.table_view)
        self.table_view.setItemDelegateForColumn(1, self.delegate)
        self.data = [
            [1, 90, 3, 4],
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            [1, 2, 3, 4]

        ]
        self.model = TableModel(self.data)
        self.table_view.setModel(self.model)

        self.add_push_button.pressed.connect(self.add)
        self.remove_push_button.pressed.connect(self.remove)
        self.start_push_button.pressed.connect(self.start)
        self.pause_push_button.pressed.connect(self.pause)
        self.threadpool = QThreadPool()

    def update_progress(self, progress):
        old_value = self.model.videos[0]
        self.model.videos[0] = [old_value[0], progress]
        self.model.dataChanged.emit(0, 0)

    def remove(self):
        print('Remove Clicked')
        return
        indexes = self.todo_list_view.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self.model.videos[index.row()]
            self.model.layoutChanged.emit()
            self.todo_list_view.clearSelection()
            self.save()

    def load(self):
        try:
            with open("data.json", 'r') as f:
                self.model.videos = json.load(f)
        except Exception:
            pass

    def save(self):
        with open("data.json", 'w') as f:
            data = json.dump(self.model.videos, f)

    def start(self):
        print('Start Clicked')
        return
        indexes = self.todo_list_view.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.videos[row]
            self.model.todos[row] = (True, text)
            self.model.dataChanged.emit(index, index)
            self.todo_list_view.clearSelection()
            self.save()

    def add(self):
        self.model.videos.append(['esg', 41])
        self.model.layoutChanged.emit()
        worker = Worker()
        worker.signals.progress.connect(self.update_progress)
        self.threadpool.start(worker)

    def pause(self):
        print('pause clicked')
        return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
