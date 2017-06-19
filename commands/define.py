# coding=utf-8
import json
import urllib
import urllib2

import xmltodict
from PyDictionary import PyDictionary

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    bot.sendMessage(chat_id=chat_id, text=get_define_data(keyConfig, user, requestText))

def get_define_data(keyConfig, user, requestText):
    formatted_entry = ''
    spellingUrl = 'https://api.cognitive.microsoft.com/bing/v5.0/spellcheck'
    values = {'text': requestText}
    data = urllib.urlencode(values)
    req = urllib2.Request(spellingUrl + '?' + data)
    req.add_header('Ocp-Apim-Subscription-Key', keyConfig.get('Bing', 'SpellCheckApiKey'))
    spellingData = json.load(urllib2.urlopen(req))
    if 'flaggedTokens' in spellingData and len(spellingData['flaggedTokens']) > 0:
        formatted_entry += 'Did you mean '
        for token in spellingData['flaggedTokens']:
            for suggestion in token['suggestions']:
                formatted_entry += suggestion['suggestion'] + ', '
        formatted_entry = formatted_entry.rstrip(', ') + '?\n'
    definition = PyDictionary.googlemeaning(requestText)
    if definition:
        formatted_entry += (user if not user == '' else 'Dave') + ', ' + definition.replace(' :', ':')
        return formatted_entry
    else:
        return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
               ', I\'m afraid I can\'t find any definitions for the word ' + requestText + '.\n' + formatted_entry
