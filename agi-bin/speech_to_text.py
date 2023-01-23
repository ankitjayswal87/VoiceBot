#!/usr/bin/env python3

import sys
import os
import json
import time
import requests
from asterisk.agi import *
#from contextlib import contextmanager
#import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk
import constants as ct

agi = AGI()

agi.verbose("Entering into Python AGI...")
agi.answer()
file_name = sys.argv[1]+'.wav'

agi.verbose('Recording FileName is %s' % file_name)

#STT from Audio File
def from_file(file_name):
    speech_config = speechsdk.SpeechConfig(subscription=ct.SUBSCRIPTION_KEY, region=ct.REGION)
    speech_config.enable_dictation()
    audio_input = speechsdk.AudioConfig(filename=file_name)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once_async().get()
    return result.text

#Classify intent and entity with Rasa query
def get_intent(data):
    import requests
    import json
    url = "http://"+ct.RASA_HOST+"/model/parse"
    intent = requests.post(url, data = '{"text":"'+data+'"}')
    intent = json.loads(intent.text)
    intent_name = intent['intent']['name']
    if len(intent['entities'])>0:
        data = intent['entities']
        entity_name = data[0]['entity']
        entity_value = data[0]['value']
    else:
        entity_name = 'none'
        entity_value = 'none'
    return intent_name+':'+entity_name+':'+entity_value

try:
    data = from_file(file_name)
    agi.verbose('The Detected Data: %s' %data)
    data = get_intent(data)
    data = data.split(':')
    intent_name = data[0]
    entity_name = data[1]
    entity_value = data[2]
    agi.set_variable('intent',intent_name)
    agi.set_variable('entity_name',entity_name)
    agi.set_variable('entity_value',entity_value)
except sr.UnknownValueError:
    agi.verbose('Google Speech Recognition could not understand audio')
    agi.set_variable('intent',bot_challenge)
    pass
except sr.RequestError as e:
    agi.verbose('Could not request results from Google Speech Recognition service')
    agi.set_variable('intent',bot_challenge)
    pass
