import os
import traceback
import time

from threading import Lock
from PyQt5.QtCore import pyqtSlot
from debug.qthread_with_logging import QThreadWithLogging

is_run_on_posix = os.name == 'posix'
capable_gpio = is_run_on_posix
if is_run_on_posix:
    import RPi.GPIO as gpio
    from omxplayer.player import OMXPlayer
    gpio.setwarnings(False)
else:
    import subprocess
    import psutil


class MusicPlayer(QThreadWithLogging):
    def __init__(self):
        QThreadWithLogging.__init__(self)
        self.playlist = []
        self.process = None
        self.process_util = None
        self.player = None
        self.lock = Lock()

        self.dbus_increment = 1
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
            if is_run_on_posix:
                self.player = OMXPlayer(mp3_path, args='--no-keys -o local',
                                        dbus_name=f'org.mpris.MediaPlayer2.omxplayer{self.dbus_increment}')
                self.dbus_increment += 1
                while self.player._process.returncode is None: time.sleep(1)
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
            if is_run_on_posix:
                self.player = OMXPlayer(mp3_path, args='--no-keys -o local',
                                        dbus_name=f'org.mpris.MediaPlayer2.omxplayer{self.dbus_increment}')
                self.dbus_increment += 1
                while self.player._process.returncode is None: time.sleep(1)
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
                if is_run_on_posix:
                    self.player.pause()
                    gpio.output(18, gpio.LOW)
                else:
                    self.process_util.suspend()
            except Exception as e:
                self.log(f'failed to pause music')
                self.log(traceback.format_exc())

    @pyqtSlot()
    def music_resume(self):
        if self.process:
            try:
                if is_run_on_posix:
                    self.player.play()
                    gpio.output(18, gpio.HIGH)
                else:
                    self.process_util.resume()
            except Exception as e:
                self.log(f'failed to pause music')
                self.log(traceback.format_exc())

    @pyqtSlot()
    def close(self):
        if self.process:
            print(self.process.terminate())
