'''
Speech synthesis using gTTS API
'''

from gtts import gTTS
from io import BytesIO
import os
import cmd

PATH = "../../tmp/"
VOICES_PATH="../../assets/voices/"


def text_to_speech(text):
    tts = gTTS(text=text, lang='fr', slow=False)
    tts.save(PATH+"file.mp3") 
    os.system("mpg123 "+PATH+"file.mp3")
    if os.path.exists(PATH+"file.mp3"):
        os.remove(PATH+"file.mp3")     #removing the mp3 file

def attente_ordre_speech():
    return text_to_speech("allez-y, dites moi ce que vous souhaitez")

def eteindre_speech():
    return text_to_speech("A")

def photo_speech():
    return text_to_speech("Quel type de photo voulez vous ? simple ou de groupe ?")

def cadrage_speech() :
    return text_to_speech("Un petit cadrage de la photo, deux secondes s'il vous plait")

def temps_presque_ecoule_speech():
    return text_to_speech("Le temps est presque écoulé")

def temps_ecoule_speech():
    return text_to_speech("Le temps est écoulé")

def play_voices(voice_name):
    os.system("mpg123 "+VOICES_PATH+voice_name+".mp3")

def happy_voice():
    return play_voices("happy")

def start_voice():
    return play_voices("start")

def prise_de_photo_voice():
    return play_voices("prise_de_photo")

def incomprehension_voice():
    return play_voices("incomprehension")

def sad_voice():
    return play_voices("triste")

def turn_of_voice():
    return play_voices("turn_off")

def prise_de_photo1():
    text_to_speech("1")
    text_to_speech("2")
    text_to_speech("3")
    
  
def prise_de_photo2():
    text_to_speech("cliic")
    prise_de_photo_voice()
    


if __name__ == '__main__':

    text_to_speech('salut, je suis reachy ! Souhaitez-vous prendre une photo ?')
    #cadrage_speech()
    #text_to_speech(cmd.one_out(cmd.set_aurevoir["s"]))