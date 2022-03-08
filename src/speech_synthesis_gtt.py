'''
Speech synthesis using gTTS API
'''

from gtts import gTTS
from io import BytesIO
import os

mp3_fp = BytesIO()
tts = gTTS(text='salut, je suis reachy ! Vous voulez une photo ?', lang='fr')
tts.write_to_fp(mp3_fp)
os.system("mpg123 ../tmp/file.mp3")
