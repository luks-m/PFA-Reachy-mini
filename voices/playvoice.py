from playsound import playsound
import random
import os

list = os.listdir('.')
list.remove("playvoice.py")
#list.remove("playsound.py~")

voice = random.choice(list)
playsound(voice)
