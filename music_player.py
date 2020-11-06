import os
import subprocess
import traceback
import signal
import psutil
from threading import Lock

from PyQt5.QtCore import pyqtSlot

from debug.qthread_with_logging import QThreadWithLogging

capable_gpio = os.name == 'posix'

if capable_gpio:
    import RPi.GPIO as gpio


class MusicPlayer(QThreadWithLogging):
    def __init__(self):
        QThreadWithLogging.__init__(self)
        self.playlist = []
        self.process = None
        self.process_util = None
        self.lock = Lock()
        if capable_gpio:
            gpio.setmode(gpio.BCM)
            gpio.setup(18, gpio.OUT)

    @pyqtSlot(list)
    def push_to_playlist(self, pathes):
        self.log(f'lock by push_to_playlist')
        with self.lock:
            self.log(f'push {pathes}')
            self.playlist += pathes
        self.log(f'unlock')

    @pyqtSlot(result=list)
    def get_playlist(self):
        self.log(f'lock by push_to_playlist')
        with self.lock:
            playlist = list(self.playlist)
        self.log(f'unlock')
        return playlist

    @pyqtSlot()
    def play_unstoppable_music(self, mp3_path):
        self.log(f'begin force playing {mp3_path}')
        if capable_gpio:
            gpio.output(18, gpio.HIGH)
        try:
            if os.name == 'posix':
                process = subprocess.Popen(f'omxplayer -o local "{mp3_path}" --no-keys', shell=True)
                process.wait()
                process.terminate()
            else:
                process = subprocess.Popen(rf'python debug\run_mp3.py "{mp3_path}"')
                process.wait()
                process.terminate()
        except:
            self.log(f'failed to force playing {mp3_path}')
            self.log(traceback.format_exc())
        if capable_gpio:
            gpio.output(18, gpio.LOW)
        self.log(f'end force playing {mp3_path}')

    @pyqtSlot()
    def play_music(self, mp3_path):
        self.log(f'begin playing {mp3_path}')
        if capable_gpio:
            gpio.output(18, gpio.HIGH)
        try:
            if os.name == 'posix':
                self.process = subprocess.Popen(f'omxplayer -o local "{mp3_path}" --no-keys', shell=True)
                self.process_util = psutil.Process(pid=self.process.pid)
                self.process.wait()
                self.process.terminate()
            else:
                self.process = subprocess.Popen(rf'python debug\run_mp3.py "{mp3_path}"')
                self.process_util = psutil.Process(pid=self.process.pid)
                self.process.wait()
                self.process.terminate()
        except:
            self.log(f'failed to playing {mp3_path}')
            self.log(traceback.format_exc())
        if capable_gpio:
            gpio.output(18, gpio.LOW)
        self.log(f'end playing {mp3_path}')

    def run(self):
        while not self.isFinished():
            if len(self.playlist) > 0:
                self.log(f'lock by running')
                with self.lock:
                    try:
                        self.play_music(self.playlist[0])
                    except:
                        self.log(traceback.format_exc())
                    del self.playlist[0]
                self.log('unlock')

    @pyqtSlot()
    def music_pause(self):
        if self.process:
            try:
                self.process_util.suspend()
                if capable_gpio:
                    gpio.output(18, gpio.LOW)
            except Exception as e:
                self.log(f'failed to pause music')
                self.log(traceback.format_exc())

    @pyqtSlot()
    def music_resume(self):
        if self.process:
            try:
                self.process_util.resume()
                if capable_gpio:
                    gpio.output(18, gpio.HIGH)
            except Exception as e:
                self.log(f'failed to pause music')
                self.log(traceback.format_exc())

    @pyqtSlot()
    def close(self):
        if self.process:
            print(self.process.terminate())
