'''
Speech synthesis using pyttsx3
'''
import pyttsx3

"""text to speech function"""
def text_to_speech(text,rate=150,volume=1.0):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume',volume)
    engine.setProperty('voice', engine.getProperty('voices')[26].id)
    engine.say(text)
    engine.runAndWait()


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
