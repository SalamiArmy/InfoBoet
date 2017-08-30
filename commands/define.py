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
    spellingUrl = 'https://od-api.oxforddictionaries.com/api/v1/search/en'
    values = {'q': requestText.lower(), 'prefix':'false'}
    data = urllib.urlencode(values)
    req = urllib2.Request(spellingUrl + '?' + data)
    req.add_header('app_id', keyConfig.get('OxfordDictionaries', 'ID'))
    req.add_header('app_key', keyConfig.get('OxfordDictionaries', 'KEY'))
    spellingData = json.load(urllib2.urlopen(req))
    if 'results' in spellingData and len(spellingData['results']) > 0:
        formatted_entry = spellingData['results'][0]['word']

        definitionUrl = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/'
        req = urllib2.Request(definitionUrl + formatted_entry.lower())
        req.add_header('app_id', keyConfig.get('OxfordDictionaries', 'ID'))
        req.add_header('app_key', keyConfig.get('OxfordDictionaries', 'KEY'))
        data = json.load(urllib2.urlopen(req))
    if data:
        pronounce = ''
        definition = ''
        if 'results' in data and len(data['results']) > 0 and 'lexicalEntries' in data['results'][0] and len(data['results'][0]['lexicalEntries']) > 0 and 'pronunciations' in data['results'][0]['lexicalEntries'][0] and len(data['results'][0]['lexicalEntries'][0]['pronunciations']) > 0 and 'audioFile' in data['results'][0]['lexicalEntries'][0]['pronunciations'][0]:
            pronounce = data['results'][0]['lexicalEntries'][0]['pronunciations'][0]['audioFile']
        if 'results' in data and len(data['results']) > 0 and 'lexicalEntries' in data['results'][0] and len(data['results'][0]['lexicalEntries']) > 0 and 'entries' in data['results'][0]['lexicalEntries'][0] and len(data['results'][0]['lexicalEntries'][0]['entries']) > 0 and 'senses' in data['results'][0]['lexicalEntries'][0]['entries'][0] and len(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses']) > 0 and 'definitions' in data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'] and len(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions']) > 0:
            definition = data['results'][0]['lexicalEntries'][0]['senses'][0]['definitions'][0]
        return (user if not user == '' else 'Dave') + ', ' + definition + '\n' + pronounce
    else:
        return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
               ', I\'m afraid I can\'t find any definitions for the word ' + requestText + '.\n' + formatted_entry
