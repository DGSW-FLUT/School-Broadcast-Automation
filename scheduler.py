import datetime
import traceback

from PyQt5.QtCore import pyqtSlot

from debug.qthread_with_logging import QThreadWithLogging
from data.schedule import schedule as entire_schedule
from threading import Lock


def get_music_for_none_buffer_case():
    weekday = datetime.datetime.now().weekday()
    return [f'audio/default_music/{weekday}/0.mp3', f'audio/default_music/{weekday}/1.mp3',
            f'audio/default_music/{weekday}/2.mp3']


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
        self.name_for_static_alarm.append('기숙사퇴실')

        self.prev = datetime.datetime(2020, 8, 1)
        self.curr = datetime.datetime.now()
        self.debug_all_around = False

        self.lock = Lock()

        for grade in ['1', '2', '3']:
            for meal in ['아침', '점심', '저녁']:
                self.name_for_static_alarm.append(f'{grade}학년{meal}')

    @pyqtSlot()
    def all_around_test(self):
        self.log(f'lock to all_around_test')
        with self.lock:
            now = datetime.datetime.now()
            self.prev = now.replace(hour=0, minute=0, second=0, microsecond=0)
            self.curr = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            self.debug_all_around = True
        self.log(f'unlock to all_around_test')

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
        elif tag == '아침운동체크':
            self.main_platform.music_player.music_pause()
            self.main_platform.music_player.play_unstoppable_music('audio/아침운동체크.mp3')
            self.main_platform.music_player.music_resume()
        elif tag in self.name_for_static_alarm:
            self.main_platform.music_player.push_to_playlist([f'audio/{tag}.mp3'])
        else:
            self.log(f'unknown command {tag}')
        self.log(f'finish {tag}')

    def run(self):
        if self.curr.date().weekday() in [5, 6]:
            self.schedule = entire_schedule['휴일']
        else:
            self.schedule = entire_schedule['평일']
        while not self.isFinished():
            with self.lock:
                if not self.debug_all_around:
                    self.curr = datetime.datetime.now()
                try:
                    if self.curr.date() != self.prev.date():
                        self.prev = self.curr
                        if self.curr.date().weekday() in [5, 6]:
                            self.schedule = entire_schedule['휴일']
                        else:
                            self.schedule = entire_schedule['평일']

                    is_trying_to_play = False
                    for certain_time in self.schedule:
                        if self.prev.time() < certain_time <= self.curr.time():
                            self.prev = datetime.datetime.combine(self.curr.date(), certain_time)
                            self.tag_decoder(self.schedule[certain_time])
                            is_trying_to_play = True
                            break

                    if self.debug_all_around and not is_trying_to_play:
                        self.debug_all_around = False
                        self.prev = datetime.datetime.now()
                        self.curr = datetime.datetime.now()
                except:
                    self.log(traceback.format_exc())
