import playsound as ps
import random
import os

list = os.listdir('.')
list.remove("playsound.py")
list.remove("playsound.py~")

voice = random.choice(list)
ps.playsound(voice)
