# coding=utf-8
import base64
import json
import urllib
import requests

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message)
    logging.info('Saying: ' + requestText)
    #print 'Saying: ' + requestText
    languageCode = 'en-GB'
    voice = 'Standard-A'
    if not send_text_as_voice(chat_id, keyConfig, requestText, voice, languageCode):
        bot.sendMessage(chat_id=str(chat_id), text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t say that.')


def send_text_as_voice(chat_id, keyConfig, requestText, voice, languageCode):
    data = get_voice(requestText, keyConfig, voice, languageCode)
    print str(data)
    if data and 'error' not in data:
        requests.post('https://api.telegram.org/bot' + keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID') +
                      '/sendVoice?chat_id=' + str(chat_id),
                      files={'voice': ('no but what I\'M saying is.ogg', data, 'audio/ogg', {'Expires': '0'})})
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
    
    try:
        raw_data = urlfetch.fetch(
            url='https://texttospeech.googleapis.com/v1beta1/text:synthesize?key=' + keyConfig.get('Google', 'GCSE_APP_ID'),
            payload=strPayload,
            method='POST',
            headers={'Content-type': 'application/json'})
    except:
        return ''
    print raw_data.content
    speechData = json.loads(raw_data.content)
    if 'error' not in speechData and 'audioContent' in speechData:
        return speechData['audioContent']
    else:
        print str(speechData)
        return str(speechData)
