# coding=utf-8
import base64
import json
import requests

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message)
    fullVoice = ['en-US-Wavenet-A',
                 'en-US-Wavenet-B',
                 'en-US-Wavenet-C',
                 'en-US-Wavenet-D',
                 'en-US-Wavenet-E',
                 'en-US-Wavenet-F',
                 'en-US-Standard-B',
                 'en-US-Standard-C',
                 'en-US-Standard-D',
                 'en-US-Standard-E',
                 'en-GB-Standard-A',
                 'en-GB-Standard-B',
                 'en-GB-Standard-C',
                 'en-GB-Standard-D',
                 'en-AU-Standard-A',
                 'en-AU-Standard-B',
                 'en-AU-Standard-C',
                 'en-AU-Standard-D']
    for voice in fullVoice:
        languageCode = voice.split('-')[0] + '-' + voice.split('-')[1]
        voice = voice.split('-')[2] + '-' + voice.split('-')[3]
        bot.sendMessage(chat_id=str(chat_id), text=str(languageCode) + "-" + str(voice) + ':')
        if not send_text_as_voice(chat_id, keyConfig, requestText, voice, languageCode):
            bot.sendMessage(chat_id=str(chat_id), text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t say that.')


def send_text_as_voice(chat_id, keyConfig, requestText, voice, languageCode):
    data = get_voice(requestText, keyConfig, voice, languageCode)

    if data and 'error' not in data:
        requests.post('https://api.telegram.org/bot' + keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID') +
                      '/sendVoice?chat_id=' + str(chat_id),
                      files={'voice': ('no but what I\'M saying is.ogg', base64.b64decode(str(data)), 'audio/ogg', {'Expires': '0'})})
        return True
    return False


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
