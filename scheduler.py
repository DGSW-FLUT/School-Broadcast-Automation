import datetime
import traceback

from PyQt5.QtCore import pyqtSlot

from qthread_with_logging import QThreadWithLogging
from res.schedule import schedule as entire_schedule


def get_music_for_none_buffer_case():
    weekday = datetime.datetime.now().weekday()
    return [f'res/default_music/{weekday}/0.mp3', f'res/default_music/{weekday}/1.mp3']


class Scheduler(QThreadWithLogging):
    last = datetime.datetime.now()

    def __init__(self, main_platform):
        QThreadWithLogging.__init__(self)
        self.main_platform = main_platform
        self.schedule = []
        self.name_for_static_alarm = []
        self.name_for_static_alarm.append('입구폐쇄')
        self.name_for_static_alarm.append('점호준비')
        self.name_for_static_alarm.append('점호시작')
        self.name_for_static_alarm.append('점호종료')
        for grade in ['1', '2', '3']:
            for meal in ['아침', '점심', '저녁']:
                self.name_for_static_alarm.append(f'{grade}학년{meal}')

    @pyqtSlot(str)
    def tag_decoder(self, tag: str):
        self.log(f'decode {tag}')
        if tag == '기상송':
            with self.main_platform.external_storage_manager.lock:
                self.log(f'getlock 기상송')
                if len(self.main_platform.external_storage_manager.files_to_play) > 0:
                    self.main_platform.music_player.push_to_playlist(
                        self.main_platform.external_storage_manager.files_to_play)
                else:
                    self.main_platform.music_player.push_to_playlist(get_music_for_none_buffer_case())
        elif tag == '기상송초기화':
            self.main_platform.external_storage_manager.clear_internal_storage()
        elif tag in self.name_for_static_alarm:
            self.main_platform.music_player.push_to_playlist([f'res/{tag}.mp3'])
        else:
            self.log(f'unknown command {tag}')
        self.log(f'finish {tag}')

    def run(self):
        prev = datetime.datetime(2020, 6, 23)
        curr = datetime.datetime.now()
        if curr.date().weekday() in [5, 6]:
            self.schedule = entire_schedule['휴일']
        else:
            self.schedule = entire_schedule['평일']
        while not self.isFinished():
            curr = datetime.datetime.now()
            try:
                if curr.date() != prev.date():
                    prev = curr
                    if curr.date().weekday() in [5, 6]:
                        self.schedule = entire_schedule['휴일']
                    else:
                        self.schedule = entire_schedule['평일']
                for certain_time in self.schedule:
                    if prev.time() < certain_time <= curr.time():
                        prev = datetime.datetime.combine(curr.date(), certain_time)
                        self.tag_decoder(self.schedule[certain_time])
            except:
                self.log(traceback.format_exc())
