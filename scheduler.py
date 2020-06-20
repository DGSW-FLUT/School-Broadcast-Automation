import datetime
import time
import traceback

from qthread_with_logging import QThreadWithLogging


class Scheduler(QThreadWithLogging):
    last = datetime.datetime.now()
    main_platform = None

    def __init__(self):
        QThreadWithLogging.__init__(self)
        self.schedule = []
        self.name_for_static_alarm = []
        self.name_for_static_alarm.append('나이스자가진단')
        self.name_for_static_alarm.append('기숙사이동')
        self.name_for_static_alarm.append('점호준비')
        self.name_for_static_alarm.append('점호시작')
        self.name_for_static_alarm.append('점호종료')
        for grade in ['1', '2', '3']:
            for meal in ['아침', '점심', '저녁']:
                self.name_for_static_alarm.append(f'{grade}학년{meal}')

    def tag_decoder(self, tag: str):
        self.log(f'decode {tag}')
        if tag == '기상송':
            time.sleep(1)
            with self.main_platform.external_storage_manager.lock:
                self.log(f'begin 기상송')
                for path in self.main_platform.external_storage_manager.files_to_play:
                    self.main_platform.music_player.play_mp3(path)
                self.log(f'end 기상송')
        elif tag in self.name_for_static_alarm:
            self.log(f'begin {tag}')
            self.main_platform.music_player.play_mp3(f'res/{tag}.mp3')
            self.log(f'end {tag}')

    def run(self):
        prev = datetime.datetime(2020, 6, 20)
        while not self.isFinished():
            curr = datetime.datetime.now()
            try:
                if curr.date() != prev.date():
                    prev = curr
                    if curr.date().weekday() in [5, 6]:
                        self.schedule = self.main_platform.entire_schedule['휴일']
                    else:
                        self.schedule = self.main_platform.entire_schedule['평일']
                for certain_time in self.schedule:
                    if prev.time() < certain_time <= curr.time():
                        prev = datetime.datetime.combine(curr.date(), certain_time)
                        self.tag_decoder(self.schedule[certain_time])
            except:
                self.log(traceback.format_exc())
