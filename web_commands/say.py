# coding=utf-8
import base64
import json
import requests

from google.appengine.api import urlfetch

def run(keyConfig, message, totalResults=1):
    requestText = str(message)
    fullVoice = ['en-GB-Standard-B']
    for voice in fullVoice:
        languageCode = voice.split('-')[0] + '-' + voice.split('-')[1]
        voice = voice.split('-')[2] + '-' + voice.split('-')[3]
        return base64.b64decode(str(get_voice(requestText, keyConfig, voice, languageCode)))

def get_voice(text, keyConfig, voice, languageCode):
    strPayload = str({
    "input": 
    {
        "text": str(text)
    },
    "voice": 
    {
        "name": str(languageCode) + "-" + str(voice),
        "languageCode": str(languageCode)
    },
    "audioConfig": 
    {
        "audioEncoding": "OGG_OPUS"
    }
})

    raw_data = urlfetch.fetch(
        url='https://texttospeech.googleapis.com/v1beta1/text:synthesize?key=' + keyConfig.get('Google', 'GCSE_APP_ID'),
        payload=strPayload,
        method='POST',
        headers={'Content-type': 'application/json'})
    speechData = json.loads(raw_data.content)
    if 'error' not in speechData and 'audioContent' in speechData:
        return speechData['audioContent']
    else:
        return str(speechData)
