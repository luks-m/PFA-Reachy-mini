from playsound import playsound
import random
import os

PATH = "./assert/voices/"

list_voice = os.listdir(PATH)
list_voice = [k for k in list_voice if '.mp3' in k]

voice = random.choice(list_voice)
playsound(PATH+voice)
