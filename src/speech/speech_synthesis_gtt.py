'''
Speech synthesis using gTTS API
'''

from gtts import gTTS
from io import BytesIO
import os

PATH = "../../tmp/"


def text_to_speech(text):
    tts = gTTS(text=text, lang='fr', slow=False)
    tts.save(PATH+"file.mp3")
    os.system("mpg123 "+PATH+"file.mp3")
    if os.path.exists(PATH+"file.mp3"):
        os.remove(PATH+"file.mp3")     #removing the mp3 file

if __name__ == '__main__':

    text_to_speech('salut, je suis reachy ! Vous voulez une photo ?')