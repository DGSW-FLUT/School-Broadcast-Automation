import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, QTimer, QStringListModel
from PyQt5.QtWidgets import QTreeWidgetItem

from external_storage_manager import ExternalStorageManager
from music_player import MusicPlayer
from res.schedule import schedule as entire_schedule
from scheduler import Scheduler


class MainWindow(QtWidgets.QMainWindow, uic.loadUiType('res/planner.ui')[0]):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 849)
        self.setupUi(self)

        self.submit.clicked.connect(self.on_input)
        self.data_edit.returnPressed.connect(self.submit.click)

        self.external_storage_manager = ExternalStorageManager()
        self.external_storage_manager.start()

        self.music_player = MusicPlayer()
        self.music_player.start()

        self.scheduler = Scheduler(self)
        self.scheduler.main_platform = self
        self.scheduler.start()

        self.log_units = [self.external_storage_manager, self.music_player, self.scheduler]

        self.checkbox_list = []
        for k in range(16):
            self.checkbox_list.append(getattr(self, f'cboxlist_item{k}'))
        for k, log_unit in enumerate(self.log_units):
            self.checkbox_list[k].setText(log_unit.log_header)
            self.checkbox_list[k].setChecked(True)
            self.checkbox_list[k].toggled.connect(lambda: self.on_toggle_cbox(self.checkbox_list[k], k))

        self.cbox_autoscroll.setChecked(True)

        self.console_log = QStringListModel()
        self.console.setModel(self.console_log)

        self.default_schedule_tree.setHeaderLabels(['일자', '시간', '행동'])
        for head in entire_schedule:
            header = QTreeWidgetItem([head])
            for tail_time in entire_schedule[head]:
                header.addChild(QTreeWidgetItem([None, str(tail_time), entire_schedule[head][tail_time]]))
            self.default_schedule_tree.addTopLevelItem(header)
            header.setExpanded(True)

        self.log_timer = QTimer()
        self.log_timer.setInterval(1000)
        self.log_timer.timeout.connect(self.on_check_log)
        self.log_timer.start()

        self.show()

    def insert_log(self, log: str):
        row = self.console_log.rowCount()
        self.console_log.insertRow(row)
        index = self.console_log.index(row)
        self.console_log.setData(index, log)

    @pyqtSlot()
    def on_toggle_cbox(self, check_box, k):
        if k < len(self.log_units):
            self.log_units[k].log_enable = check_box.isChecked()

    @pyqtSlot()
    def on_input(self):
        text = self.data_edit.text()
        self.parse_command(text.lower())
        self.console.scrollToBottom()
        self.data_edit.setText('')

    @pyqtSlot()
    def on_check_log(self):
        logs_to_insert = []
        for k, log_unit in enumerate(self.log_units):
            if log_unit.is_empty():
                continue
            for log in log_unit.flush_log():
                logs_to_insert.append(log)
        if len(logs_to_insert) > 0:
            logs_to_insert.sort(key=lambda x: x[0])
            for log in logs_to_insert:
                self.insert_log('%02d:%02d: %s' % (log[0].hour, log[0].minute, log[1].replace(os.getcwd(), '$://')))
            if self.cbox_autoscroll.isChecked():
                self.console.scrollToBottom()

    def parse_command(self, command: str):
        self.insert_log(f'>> {command}')
        if command == 'test':
            self.music_player.play_mp3('res/테스트.mp3')
        elif command.startswith('-'):
            self.scheduler.tag_decoder(command[1:])
        self.insert_log(f'<< {command}')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main = MainWindow()
    main.show()
    app.exec_()
