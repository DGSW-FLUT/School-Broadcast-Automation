import os
import shutil
import subprocess
import time
import traceback
import datetime
from threading import Lock

from debug.qthread_with_logging import QThreadWithLogging

is_posix = os.name == 'posix'

MUSIC_COUNT = 3


def get_default_music():
    weekday = datetime.datetime.now().weekday()
    return [f'audio/default_music/{weekday}/{k}.mp3' for k in range(MUSIC_COUNT)]


def get_available_external_storage_list():
    external_storage_list = []
    if is_posix:
        external_storage_list = os.listdir('/media/pi')
    else:
        process = subprocess.Popen('wmic logicaldisk get name,description', shell=True, stdout=subprocess.PIPE)
        res, err = process.communicate()
        if err is not None:
            return []
        for k, line in enumerate(res.split(b'\r\n')):
            if k > 0:
                desc = line[:16]
                letter = line[18:20]
                if desc == b'\xc0\xcc\xb5\xbf\xbd\xc4 \xb5\xf0\xbd\xba\xc5\xa9   ':
                    external_storage_list.append(f'{letter.decode()}\\')
    return external_storage_list


class StorageManager(QThreadWithLogging):
    old_external_storage_list = []
    files_to_store = []
    lock = Lock()

    def __init__(self):
        QThreadWithLogging.__init__(self)
        self.store_path = os.getcwd() + '/buffer/'

    def clear_internal_storage(self):
        self.log('clear_IntStorage')
        for file in os.listdir(self.store_path):
            if file.startswith('.'):
                continue
            os.remove(self.store_path + file)

    def store_from_external_storage(self, load_path):
        self.log('store_IntStorage_from_ExtStorage')
        for k, file in enumerate(self.files_to_store):
            self.log(f'store_IntStorage_from_ExtStorage {file}')
            shutil.copyfile(load_path + file, self.store_path + f'{k}.mp3')

    @property
    def files_to_play(self):
        result = []
        for name in os.listdir(self.store_path):
            if not os.path.isfile(self.store_path + name):
                continue
            if name.endswith('.mp3') or name.endswith('.mp4'):
                if name[0] in ('.', '$', '~'):
                    continue
                result.append(self.store_path + name)
        result.sort()
        default_music = get_default_music()
        while len(result) < MUSIC_COUNT:
            result.append(default_music[len(result)])
        return result

    def run(self):
        while not self.isFinished():
            try:
                new_external_storage_list = get_available_external_storage_list()
                if self.old_external_storage_list != new_external_storage_list:
                    self.old_external_storage_list = new_external_storage_list
                    self.log('detect_ExtStorage_change')
                    if len(new_external_storage_list) > 0:
                        time.sleep(5)
                        self.log('lock')
                        with self.lock:
                            if is_posix:
                                load_path = '/media/pi/' + new_external_storage_list[0] + '/'
                            else:
                                load_path = new_external_storage_list[0]
                            self.files_to_store = [
                                name for name in os.listdir(load_path)
                                if os.path.isfile(load_path + name) and
                                   name.endswith('.mp3') and
                                   name[0] not in ('.', '$', '~')
                            ]
                            self.files_to_store.sort()
                            self.clear_internal_storage()
                            self.store_from_external_storage(load_path)
                        self.log('unlock')
                    else:
                        self.log('can\'t detect ExtStorage')
                else:
                    time.sleep(5)
            except:
                self.log(traceback.format_exc())
