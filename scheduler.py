import datetime
import traceback

from qthread_with_logging import QThreadWithLogging
from res.schedule import schedule as entire_schedule


class Scheduler(QThreadWithLogging):
    last = datetime.datetime.now()
    music_for_none_buffer_case = ['res/loona oec-sweet crazy love.mp3', 'res/loona-ding ding dong.mp3']

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

    def tag_decoder(self, tag: str):
        self.log(f'decode {tag}')
        if tag == '기상송':
            with self.main_platform.external_storage_manager.lock:
                self.log(f'begin 기상송')
                if len(self.main_platform.external_storage_manager.files_to_play) > 0:
                    for path in self.main_platform.external_storage_manager.files_to_play:
                        self.main_platform.music_player.push_to_playlist(path)
                else:
                    for path in self.music_for_none_buffer_case:
                        self.main_platform.music_player.push_to_playlist(path)
                self.log(f'end 기상송')
        elif tag in self.name_for_static_alarm:
            self.log(f'begin {tag}')
            self.main_platform.music_player.play_mp3(f'res/{tag}.mp3')
            self.log(f'end {tag}')

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
