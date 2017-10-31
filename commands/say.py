import base64
import json
import urllib
import requests

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.encode('utf-8')
    if '<voice-transformation' in requestText or '<express-as' in requestText:
        voice = 'en-US_AllisonVoice'
    else:
        voice = 'en-US_LisaVoice'
    if not send_text_as_voice(chat_id, keyConfig, requestText, voice):
        bot.sendMessage(chat_id=str(chat_id), text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t say that.')


def send_text_as_voice(chat_id, keyConfig, requestText, voice):
    data = get_voice(requestText, keyConfig, voice)
    if data:
        if 'error' not in data:
            requests.post('https://api.telegram.org/bot' + keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID') +
                          '/sendVoice?chat_id=' + str(chat_id),
                          files={'voice': ('no but what I\'M saying is.ogg', data, 'audio/ogg', {'Expires': '0'})})
            return True
        else:
            print json.loads(data)['description']
    return False


def get_voice(text, keyConfig, voice):
    IBMusername = keyConfig.get('IBM', 'username')
    IBMpassword = keyConfig.get('IBM', 'password')
    args = urllib.urlencode({'text': text,
                             'voice': voice,
                             'caption': voice})
    return urlfetch.fetch('https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize?' + args,
                          headers={'Authorization':'Basic %s' %
                                                   base64.b64encode(IBMusername + ':' + IBMpassword)}).content

