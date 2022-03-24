'''
Speech synthesis using gTTS API
'''

from gtts import gTTS
from io import BytesIO
import os

PATH = "./tmp/"

def text_to_speech_gtt(text):

    mp3_fp = BytesIO()
    tts = gTTS(text, lang='fr')
    tts.write_to_fp(mp3_fp)
    os.system("mpg123 ./tmp/file.mp3")

    if os.path.exists(PATH+"file.mp3"):
        os.remove(PATH+"file.mp3")     #removing the mp3 file

if __name__ == '__main__':

    text_to_speech_gtt('salut, je suis reachy ! Vous voulez une photo ?')