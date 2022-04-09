import speech_recognition as sr
from scipy.io import wavfile
import noisereduce as nr 

WAV_OUTPUT_FILENAME = "../tmp/enregistrement.wav"
WAV_OUTPUT_REDUCED_FILENAME = "../tmp/enregistrement_reduce_noise.wav"

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
        r.adjust_for_ambient_noise(source, duration=2) #  
        debug_print('Parle !')
        audio = r.listen(source,phrase_time_limit=5)
        with open(WAV_OUTPUT_FILENAME, "wb") as f:
            f.write(audio.get_wav_data())
        debug_print('Fin !')
    try:
        rate, data = wavfile.read(WAV_OUTPUT_FILENAME)
        reduced_noise = nr.reduce_noise(y=data, sr=rate)
        wavfile.write(WAV_OUTPUT_REDUCED_FILENAME, rate, reduced_noise)
        enregistrement_r_n = sr.AudioFile(WAV_OUTPUT_REDUCED_FILENAME)
        with enregistrement_r_n as source:
            better_audio = r.record(source)
        query = r.recognize_google(better_audio, language = 'fr-FR')
        debug_print(query.lower())
        return query.lower()
    except:
        return "ERROR"


