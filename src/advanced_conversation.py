import os
import openai
import json
import sys
sys.path.append("../speech")
sys.path.append("../recognition")
import speech_synthesis_gtt as speech
import vocal_recognition as vr

def openai_speech(str):
  
  openai.api_key="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"

  var=""
      
  dialog = str

  start_sequence = "\nAI:"
  restart_sequence = "\nHuman: "
  response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=dialog ,
    temperature=0.9,
    max_tokens=480,
    best_of=4,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
  )
  var=response.get("choices")[0].get("text")
  dialog+=var
  dialog+="\n"
  # y = json.loads(response.get("choices"))
  # print(y["text"])
  # print(type(response.get("choices")[0]))

  speech.text_to_speech(var[3:])
  return dialog
