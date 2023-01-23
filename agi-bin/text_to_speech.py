#!/usr/bin/env python3

import sys
import uuid
import os
import json
import time
import requests
import urllib.parse
from asterisk.agi import *
import azure.cognitiveservices.speech as speechsdk
import constants as ct

#agi = AGI()

#agi.verbose("Entering into Python AGI...")
#agi.answer()
value1 = sys.argv[1]
name = sys.argv[2]
appointment_date = urllib.parse.unquote(sys.argv[3])

#agi.verbose('Value1 is %s' % value1)
#agi.verbose('Value2 is %s' % value2)

def text_to_speech(data,filename):
    speech_config = speechsdk.SpeechConfig(subscription=ct.SUBSCRIPTION_KEY, region=ct.REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(filename="/tmp/"+filename+".wav")
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(data).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return filename
    else:
        filename='thank_you-8khz'
        return filename

temp_uuid = uuid.uuid1()
data = "Thank you, "+name+" your appointment has been booked now on "+appointment_date+" Your booking id is 3 5 4 7"
#temp_filename = text_to_speech(data,str(temp_uuid))
temp_filename = text_to_speech(data,str(value1))
#agi.set_variable('temp_filename',temp_filename)

