import traceback
from pytube import YouTube
import requests
import json
from datetime import datetime, timedelta
from debug.delegate_logging import DelegateLogging


class MusicDownloader(DelegateLogging):

    def _get_header_for_request_wake_songs(self):
        headers = {}
        headers['Host'] = 'dodam.b1nd.com'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'
        headers['Accpet'] = 'application/json, text/plain, */*'
        headers['Accpt-Language'] = 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3'
        headers['Accpet-Encoding'] = 'gzip, deflate'
        headers['Connection'] = 'keep-alive'
        headers['Referer'] = 'http://dodam.b1nd.com/wakesong'
        headers['Pragma'] = 'no-cache'
        headers['Cache-Control'] = 'no-cache'
        return headers

    def _get_music_url_list(self):
        now = datetime.now()
        target = datetime.now()
        if now.hour > 12:
            target = datetime.now() + timedelta(days=1)

        res = requests.request('GET',
                               f'http://dodam.b1nd.com/api/v2/wakeup-song?year={target.year}&month={target.month}&date={target.day}',
                               headers=self._get_header_for_request_wake_songs())
        if not res.ok:
            self.log('Failed to Get music list because of status code ', res.status_code)
            return
        res = json.loads(res.content.decode('utf-8'))
        return [row['videoUrl'] for k, row in enumerate(res['data']['allow'])]

    def download(self):
        music_list = self._get_music_url_list()
        all_music_count = len(music_list)
        self.log(f'start downloads {all_music_count}')
        try:
            for k, music_URL in enumerate(music_list):
                self.log(f'start download {k + 1}/{all_music_count} {music_URL}')
                try:
                    YouTube(music_URL).streams.filter(only_audio=True, mime_type='audio/mp4').first() \
                        .download(output_path=f'buffer', filename=f'{k}')
                    self.log(f'finish download {k + 1}/{all_music_count} {music_URL}')
                except:
                    self.log(f'failed download {k + 1}/{all_music_count} {music_URL}')

        except:
            self.log('failed downloads')
            self.log(traceback.format_exc())
        self.log('finish downloads')
