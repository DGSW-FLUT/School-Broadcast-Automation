import datetime
import traceback

from PyQt5.QtCore import pyqtSlot
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1

from qthread_with_logging import QThreadWithLogging


class Speaker(QThreadWithLogging):
    ibm_tts_service_url = 'https://gateway-seo.watsonplatform.net/text-to-speech/api'

    def __init__(self, main_platform):
        QThreadWithLogging.__init__(self)
        self.main_platform = main_platform
        self.ibm_tts_adapter = None
        self.connect_ibm()

    def connect_ibm(self):
        try:
            apikey = open('.env/ibm_apikey', 'r').read()
            self.ibm_tts_adapter = TextToSpeechV1(authenticator=IAMAuthenticator(apikey))
            self.ibm_tts_adapter.set_service_url(self.ibm_tts_service_url)
        except:
            self.ibm_tts_adapter = None
            self.log(traceback.format_exc())

    @pyqtSlot(str)
    def speak(self, letter):
        if self.ibm_tts_adapter is None:
            self.connect_ibm()
            if self.ibm_tts_adapter is None:
                return
        try:
            file_name = f'tts_buffer/{datetime.datetime.now()}.mp3'.replace(':', '-')
            with open(file_name, 'wb') as audio_file:
                audio_file.write(
                    self.ibm_tts_adapter.synthesize(
                        letter,
                        voice='ko-KR_YoungmiVoice',
                        accept='audio/mp3'
                    ).get_result().content
                )
            self.main_platform.music_player.play_mp3(file_name)

        except:
            self.ibm_tts_adapter = None
            self.log(traceback.format_exc())
