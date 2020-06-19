import os
import datetime
import shutil
import subprocess

load_path = '/home/pi/Desktop/buffer/'

last = datetime.datetime.now()
sleeping = True
weekday_ranges = [datetime.time(hour=6, minute=17), datetime.time(hour=7, minute=57)]
weekend_ranges = [datetime.time(hour=7, minute=27)]


def get_range(now):
    if now.date().weekday() in [5, 6]:
        return weekend_ranges
    return weekday_ranges


def run_mp3(files):
    print('load', files)
    for k, file in enumerate(files):
        print('play', file)
        p = subprocess.Popen('omxplayer -o local ' + load_path + str(k) + '.mp3 --no-keys', shell=True)
        p.wait()
        p.terminate()
        print('end', file)
    print('unload', files)


def clear_buffer():
    files = os.listdir(load_path)
    print('clear', files)
    for file in files:
        os.remove(load_path + file)


def copy_buffer(root_path, files):
    for k, file in enumerate(files):
        shutil.copyfile(root_path + file, load_path + str(k) + '.mp3')


usb_list = []
files = []
print('start')
while True:
    new_usb_list = os.listdir('/media/pi')
    now = datetime.datetime.now()
    if usb_list != new_usb_list:
        usb_list = new_usb_list
        if len(usb_list) > 0:
            root_path = '/media/pi/' + usb_list[0] + '/'
            files = [name for name in os.listdir(root_path) if
                     os.path.isfile(root_path + name) and name.endswith('.mp3')]
            clear_buffer()
            copy_buffer(root_path, files)
    else:
        if now.date() > last.date():
            last = now
        for span in get_range(now):
            if last.time() < span <= now.time():
                last = now
                print('play')
                try:
                    run_mp3(files)
                except Exception as e:
                    print('exception5', e)
