import speech_recognition as sr
from scipy.io import wavfile
import noisereduce as nr 

import pvporcupine
import pyaudio
import struct

WAV_OUTPUT_FILENAME = "../../tmp/enregistrement.wav"
WAV_OUTPUT_REDUCED_FILENAME = "../../tmp/enregistrement_reduce_noise.wav"

def debug_print(str):
    print("DEBUG : " + str)

# a function to create a Recognizer object (needed for speech recognition) and return a Microphone object
def init_record():
    rec = sr.Recognizer()
    with sr.Microphone()  as source:
        rec.adjust_for_ambient_noise(source, duration=2)
        return (rec, source)

# a function that record audio until "Hey Reachy" is said
def hey_reachy_detection():
    # create a pvporcupine object which is to detect keywords
    ppn = pvporcupine.create(
        access_key="4OYeOdXigB8uccAoUJWSvJqXsGXGeuKdDxX7ebkIxPVaOzQpWdMmew==",
        # path to the file that contains informations for the pvporcupine to detect Hey Reachy
        keyword_paths = ['../../assets/Hey-Reachy_en_linux_v2_1_0.ppn']
    )

    # create a PyAudio object in order to listen to the microphone and record voice
    py_audio = pyaudio.PyAudio()
    audio_stream = py_audio.open(
        rate=ppn.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=ppn.frame_length
    )

    # While we have not detected Hey Reachy
    while True:
        # read the audio frame
        pcm = audio_stream.read(ppn.frame_length)
        # unpack the audio from to fit with pvporcupine librairy
        audio_frame = struct.unpack_from("h" * ppn.frame_length, pcm)
        # try to detect the keyword in the audio frame 
        keyword_index = ppn.process(audio_frame)
        # if the keyword is detected
        if keyword_index == 0:
            ppn.delete()
            return 1


# a function that record the audio from the default microphone and transcript 
# the speech into a sentence
#
# RETURN : the transcripted speech on success (string in lower case) 
#           ; the string "ERROR" otherwise
def record_and_transcript(rec, mic):
    with mic as source:
        debug_print('Parle !')
        # record the microphone during 5 seconds 
        audio = rec.listen(source,phrase_time_limit=5)
        # write the recorded audio into a .wav file
        with open(WAV_OUTPUT_FILENAME, "wb") as f:
            f.write(audio.get_wav_data())
        debug_print('Fin !')
        try:
            rate, data = wavfile.read(WAV_OUTPUT_FILENAME)
            # reduce the noise into the .wav file
            reduced_noise = nr.reduce_noise(y=data, sr=rate)
            # write the .wav file with reduced noise in other .wav file
            wavfile.write(WAV_OUTPUT_REDUCED_FILENAME, rate, reduced_noise)
            enregistrement_r_n = sr.AudioFile(WAV_OUTPUT_REDUCED_FILENAME)
            # transform the improved .wav file to fit the speech recognition API
            with enregistrement_r_n as source:
                better_audio = rec.record(source)
            # transcript the audio by sending it to Google
            query = rec.recognize_google(better_audio, language = 'fr-FR')
            debug_print(query.lower())
            return query.lower()
        except:
            return "ERROR"



