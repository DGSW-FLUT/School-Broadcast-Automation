import os
import traceback

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSlot, QTimer, QStringListModel, QModelIndex
from PyQt5.QtWidgets import QTreeWidgetItem, QPushButton

from external_storage_manager import ExternalStorageManager
from music_player import MusicPlayer
from data.quick_macros import quick_macros
from data.schedule import schedule as entire_schedule
from scheduler import Scheduler

global main
main = None


def create_quick_macro_button(k, macro_name, macro_command):
    global main
    button = QPushButton(f'button_list_item{k}')
    button.setText(macro_name)

    @button.clicked.connect
    @pyqtSlot()
    def on_quick_marco_button_click():
        main.parse_command(macro_command)

    main.button_list.addWidget(button)
    setattr(main, f'button_list_item{k}', button)


def qt_message_handler(mode, context, message):
    if mode == QtCore.QtInfoMsg:
        mode = 'INFO'
    elif mode == QtCore.QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCore.QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtCore.QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    print(f'qt_message_handler: line: {context.line}, func: {context.function}(), file: {context.file}')
    print(f'QT->  {mode}: {message}')


QtCore.qInstallMessageHandler(qt_message_handler)


class MainWindow(QtWidgets.QMainWindow, uic.loadUiType('data/planner.ui')[0]):
    def __init__(self):
        global main
        super().__init__()
        main = self
        self.setupUi(self)

        self.submit.clicked.connect(self.on_input)
        self.data_edit.returnPressed.connect(self.submit.click)

        self.external_storage_manager = ExternalStorageManager()
        self.external_storage_manager.start()

        self.music_player = MusicPlayer()
        self.music_player.start()

        self.scheduler = Scheduler(self)
        self.scheduler.start()

        self.log_units = [self.external_storage_manager, self.music_player, self.scheduler]

        self.checkbox_list = []
        for k in range(16):
            self.checkbox_list.append(getattr(self, f'checkbox_list_item{k}'))
        for k, log_unit in enumerate(self.log_units):
            self.checkbox_list[k].setText(log_unit.log_header)
            self.checkbox_list[k].setChecked(True)
            self.checkbox_list[k].toggled.connect(lambda: self.on_toggle_checkbox(self.checkbox_list[k], k))

        self.checkbox_list_autoscroll.setChecked(True)

        self.console_log = QStringListModel()
        self.console.setModel(self.console_log)

        self.schedule_tree.setHeaderLabels(['일자', '시간', '행동'])
        for head in entire_schedule:
            header = QTreeWidgetItem([head])
            for tail_time in entire_schedule[head]:
                header.addChild(QTreeWidgetItem([None, str(tail_time), entire_schedule[head][tail_time]]))
            self.schedule_tree.addTopLevelItem(header)
            header.setExpanded(True)
        self.schedule_tree.doubleClicked.connect(self.on_double_click_schedule_tree)

        for k, macro_name in enumerate(quick_macros):
            create_quick_macro_button(k, macro_name, quick_macros[macro_name])

        self.log_timer = QTimer()
        self.log_timer.setInterval(1000)
        self.log_timer.timeout.connect(self.on_check_log)
        self.log_timer.start()

        self.show()

    def closeEvent(self, c):
        print('Closing...')
        self.log_timer.stop()
        for log_unit in self.log_units:
            log_unit.close()
            log_unit.quit()

    def insert_log(self, log: str):
        row = self.console_log.rowCount()
        self.console_log.insertRow(row)
        index = self.console_log.index(row)
        self.console_log.setData(index, log)

    @pyqtSlot(QModelIndex)
    def on_double_click_schedule_tree(self, index):
        try:
            key = index.model().data(index, 2)
            if key is not None:
                self.parse_command(f'-{key}')
        except:
            self.insert_log(traceback.format_exc())

    @pyqtSlot()
    def on_toggle_checkbox(self, check_box, k):
        if k < len(self.log_units):
            self.log_units[k].log_enable = check_box.isChecked()

    @pyqtSlot()
    def on_input(self):
        text = self.data_edit.text()
        self.parse_command(text.lower())
        self.console.scrollToBottom()
        self.data_edit.setText('')

        for k, method_name in enumerate(quick_macros):
            button = getattr(self, f'button_list_item{k}')
            print(button.x(), button.y())

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
            if self.checkbox_list_autoscroll.isChecked():
                self.console.scrollToBottom()

    @pyqtSlot(str)
    def parse_command(self, command: str):
        self.insert_log(f'>> {command}')
        try:
            if command == 'test':
                self.music_player.music_pause()
                self.music_player.play_unstoppable_music('audio/테스트.mp3')
                self.music_player.music_resume()
            elif command == 'get_musics':
                with self.external_storage_manager.lock:
                    files_to_store = self.external_storage_manager.files_to_store
                    if len(files_to_store) > 0:
                        self.insert_log('=================현재 기상송===============\n' +
                                        str(files_to_store)[1:-1].replace(',', '\n') + '\n' +
                                        '=========================================')
                    else:
                        self.insert_log('=================현재 기상송===============\n(없음, 기본 기상곡)\n' +
                                        '========================================='
                                        )
            elif command == 'all_around_test':
                self.scheduler.all_around_test()
            elif command == 'abort_song':
                self.music_player.process.terminate()
                self.music_player.process = None
                self.music_player.process_util = None
            elif command.startswith('-'):
                self.scheduler.tag_decoder(command[1:])
            else:
                self.insert_log(f'?? {command}')

        except:
            self.insert_log(traceback.format_exc())
        self.insert_log(f'<< {command}')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main = MainWindow()
    main.show()
    app.exec_()
