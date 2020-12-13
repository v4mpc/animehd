from PyQt5.QtCore import Qt, QObject, QRunnable, QThreadPool, QTimer, pyqtSignal, pyqtSlot
import time


class WorkerKilledException(Exception):
    pass


class WorkerSignals(QObject):
    progress = pyqtSignal(int, int)


class Worker(QRunnable):
    def __init__(self, job_id):
        super().__init__()
        self.signals = WorkerSignals()
        self.is_killed = False
        self.is_paused = False
        self.progress = 0
        self.job_id = job_id

    @pyqtSlot()
    def run(self):
        try:
            while self.progress < 100:
                self.progress += 10
                self.signals.progress.emit(self.job_id, self.progress)
                print('Progress emited')
                time.sleep(1)
                if self.is_killed:
                    raise WorkerKilledException
        except WorkerKilledException:
            pass

    def kill(self):
        self.is_killed = True
