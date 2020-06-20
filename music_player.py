import os
import subprocess
import time
import traceback
from threading import Lock

from PyQt5.QtCore import pyqtSlot

from qthread_with_logging import QThreadWithLogging

if os.name == 'nt':
    import pygame

    pygame.mixer.init()


class MusicPlayer(QThreadWithLogging):
    def __init__(self):
        QThreadWithLogging.__init__(self)
        self.playlist = []
        self.lock = Lock()

    @pyqtSlot(str)
    def push_to_playlist(self, path):
        self.log(f'lock by push_to_playlist')
        with self.lock:
            self.log(f'push {path}')
            self.playlist.append(path)
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
        if os.name == 'posix':
            process = subprocess.Popen(f'omxplayer -o local {mp3_path} --no-keys', shell=True)
            process.wait()
            process.terminate()
        else:
            time.sleep(1)
            pygame.mixer.music.load(f'{mp3_path}')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy(): pass
        self.log(f'end playing {mp3_path}')

    def run(self):
        while not self.isFinished():
            if len(self.playlist) > 0:
                self.log(f'lock by running')
                with self.lock:
                    try:
                        self.play_mp3(self.playlist[0])
                        del self.playlist[0]
                    except:
                        self.log(traceback.format_exc())
                self.log('unlock')
