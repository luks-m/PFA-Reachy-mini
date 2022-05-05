import os
import openai
import json
import sys
sys.path.append("../speech")
sys.path.append("../recognition")
import speech_synthesis_gtt as speech
import vocal_recognition as vr

# a function to generate conversation with the GPT-3 AI 
# it takes a string representing a conversation and return the string with the AI answer concatenate
# it also say the sentences thanks to gtt
def openai_speech(str):
  # key to access to GTP-3
  openai.api_key="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"

  # the string that will stock the AI answer
  var=""

  # the string containing the conversation
  dialog = str

  # the delimiter of the AI sentences
  start_sequence = "\nAI:"
  # the delimiter of the Human sentences
  restart_sequence = "\nHuman: "
  # create a set of answers 
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=dialog ,
    temperature=0.9,
    max_tokens=100,
    best_of=4,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
  )
  # choose one of the generated answers
  var=response.get("choices")[0].get("text")
  # add the AI answer to the conversation 
  dialog+=var
  dialog+="\n"

  # make the robot says the generated answer
  speech.text_to_speech(var[3:])
  return dialog
