'''
Speech synthesis using pyttsx3
'''
import pyttsx3

'''
text to speech function
'''
def text_to_speech(text,rate=150,volume=1.0):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume',volume)
    engine.setProperty('voice', engine.getProperty('voices')[26].id)
    engine.say(text)
    engine.runAndWait()

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


if __name__ == '__main__':

    """object creation"""
    engine = pyttsx3.init()

    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    print ("rate = ",rate)              # printing current voice rate
    engine.setProperty('rate', 150)     # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    print ("volume = ",volume)    
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    voice = engine.getProperty('voices')[26]
    print(voice)
    engine.setProperty('voice', voice.id)

    """PLaying sound directly"""
    print("saying : << Salut ! Je suis Reachy >> \n...")
    engine.say("Salut ! Je suis Reachy.")
    engine.runAndWait()

    """Saving Voice to a file"""
    print("saving voice to the file: ./test1.mp3\n...")
    engine.save_to_file('Salut ! Je suis Reachy.','test1.mp3') #make sure that 'espeak' and 'ffmpeg' are installed
    engine.runAndWait()

    text_to_speech("Au revoir !")
