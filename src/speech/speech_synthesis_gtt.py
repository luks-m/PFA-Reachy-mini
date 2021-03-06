'''
Speech synthesis using gTTS API
'''

from gtts import gTTS
from io import BytesIO
import os
import cmd

PATH = "../../tmp/"
VOICES_PATH="../../assets/voices/"

#Convert a text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='fr', slow=False)
    tts.save(PATH+"file.mp3")
    os.system("mpg123 "+PATH+"file.mp3") #Creating the mp3 file
    if os.path.exists(PATH+"file.mp3"):
        os.remove(PATH+"file.mp3")       #Removing the mp3 file
        
'''
The following functions are implemented to be associated with different states and transitions of the robot
'''

def attente_ordre_speech():
    return text_to_speech("Allez-y, dites moi ce que vous souhaitez")

def attente_ordre_aruco_speech():
    return text_to_speech("Allez-y, montrez moi un code Aruco")

def eteindre_speech():
    return text_to_speech("A")

def photo_speech():
    return text_to_speech("Quel type de photo voulez vous ? simple ou de groupe ?")

def filtre_speech():
    return text_to_speech("Quel type de filtre voulez vous ? echange de visage ou noir et blanc ?")
    
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
    text_to_speech("cheese")
    prise_de_photo_voice()
