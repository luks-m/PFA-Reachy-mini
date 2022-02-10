import speech_recognition as sr
from scipy.io import wavfile
import noisereduce as nr 


def debug_print(str):
    print("DEBUG : " + str)

# a function that record the audio from the default microphone and transcript 
# the speech into a sentence
#
# RETURN : the transpricted speech on success (string in lower case) 
#           ; the string "ERROR" otherwise
def record_and_transcript():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5) #  
        debug_print('Parle !')
        audio = r.listen(source)
        with open("enregistrement.wav", "wb") as f:
            f.write(audio.get_wav_data())
        debug_print('Fin !')
    try:
        rate, data = wavfile.read("enregistrement.wav")
        reduced_noise = nr.reduce_noise(y=data, sr=rate)
        wavfile.write("enregistrement_reduce_noise.wav", rate, reduced_noise)
        enregistrement_r_n = sr.AudioFile("enregistrement_reduce_noise.wav")
        with enregistrement_r_n as source:
            better_audio = r.record(source)
        query = r.recognize_google(better_audio, language = 'fr-FR')
        debug_print(query.lower())
        return query.lower()
    except:
        return "ERROR"

