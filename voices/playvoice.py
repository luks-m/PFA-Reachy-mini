from playsound import playsound
import random
import os

list_voice = os.listdir('.')
list_voice = [k for k in list_voice if '.mp3' in k]
#list_voice.remove("playvoice.py")
#list_voice.remove("playvoice.py~")

voice = random.choice(list_voice)
playsound(voice)
