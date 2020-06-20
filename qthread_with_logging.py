import datetime

from PyQt5.QtCore import QThread, pyqtSlot


class QThreadWithLogging(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.log_header = self.__class__.__name__
        self.log_queue = []
        self.log_enable = True

    def log(self, text):
        if self.log_enable:
            self.log_queue.append((datetime.datetime.now(), f'{self.log_header}: {text}'))

    @pyqtSlot(result=bool)
    def is_empty(self):
        return len(self.log_queue) == 0

    @pyqtSlot(result=list)
    def flush_log(self):
        data = self.log_queue
        self.log_queue = []
        return data

    @pyqtSlot(bool)
    def set_log_feature(self, enable):
        self.log_enable = enable
