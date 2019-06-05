# coding=utf-8
import base64
import json
import requests

from bs4 import BeautifulSoup

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message)
    if ('.' in requestText and ' ' not in requestText):
        requestText = getUrlText(requestText);
    fullVoice = ['en-GB-Standard-B']
    for voice in fullVoice:
        languageCode = voice.split('-')[0] + '-' + voice.split('-')[1]
        voice = voice.split('-')[2] + '-' + voice.split('-')[3]
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

def getUrlText(urlToSay):
    soup = BeautifulSoup(urlfetch.fetch(
        url=urlToSay,
        method='GET'
    ).content, 'html.parser')

    allElements = soup.recursiveChildGenerator()
    sayableElements = []
    if allElements is not None:
        for elem in allElements:
            if elem.string != None and ' ' in elem.string and elem.string.count('.') > 1 and '{' not in elem.string:
                sayableElements.append(elem.string)
    if sayableElements:
        return ' '.join(sayableElements)\
            .replace('.\n', ' ')\
            .replace('\n', '')\
            .encode('utf8')[0:4999]
    return urlToSay
