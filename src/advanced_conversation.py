import os
import openai
import json
import sys
sys.path.append("../speech")
sys.path.append("../recognition")
import speech_synthesis_gtt as speech
import vocal_recognition as vr

'''

#This is a function that takes a sentence from the user as input
#and returns the response of Reachy based on openai

Here are some informations about the parameteres used:

    #engine="text-davinci-002": the engine or the model that will generate the completion "the response"
    #prompt: the sentence that the user will be prompted to say
    #temperature: this parameter is used to control the diversity and randomness of the response,
                the higher the temperature, the more diverse the response.
    #max_tokens: the maximum number of tokens that the response can have
    #best_of: the number of best responses that will be returned
    #top_p: the probability threshold that will be used to filter the responses
    #frequency_penalty: the penalty that will be applied to the responses that are too frequent,
                  it decreases the probability of the responses that are too frequent
    #presence_penalty: the penalty that will be applied to the responses that are too short,
                  it increases the likelihood of the model to talk about new topics

'''

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
    max_tokens=50,
    best_of=1,
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
