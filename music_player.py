import os
import subprocess
import traceback
from threading import Lock

from PyQt5.QtCore import pyqtSlot

from qthread_with_logging import QThreadWithLogging

if os.name == 'nt':
    import pygame

    pygame.mixer.init()
else:
    import RPi.GPIO as gpio


class MusicPlayer(QThreadWithLogging):
    def __init__(self):
        QThreadWithLogging.__init__(self)
        self.playlist = []
        self.lock = Lock()
        if os.name == 'posix':
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
    def play_mp3(self, mp3_path):
        self.log(f'begin playing {mp3_path}')
        try:
            if os.name == 'posix':
                gpio.output(18, gpio.HIGH)
                process = subprocess.Popen(f'omxplayer -o local "{mp3_path}" --no-keys', shell=True)
                process.wait()
                process.terminate()
                gpio.output(18, gpio.LOW)
            else:
                pygame.mixer.music.load(f'{mp3_path}'.replace('/', '\\'))
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy(): pass
        except:
            self.log(traceback.format_exc())
        self.log(f'end playing {mp3_path}')

    def run(self):
        while not self.isFinished():
            if len(self.playlist) > 0:
                self.log(f'lock by running')
                with self.lock:
                    try:
                        self.play_mp3(self.playlist[0])
                    except:
                        self.log(traceback.format_exc())
                    del self.playlist[0]
                self.log('unlock')
