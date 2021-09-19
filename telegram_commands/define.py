# coding=utf-8
import ConfigParser
import json
import urllib
import urllib2
from urllib2 import HTTPError
from werkzeug.exceptions import BadRequest

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    if requestText != '':
        try:
            bot.sendMessage(chat_id=chat_id, text=get_define_data(user, requestText), parse_mode='Markdown')
        except BadRequest:
            bot.sendMessage(chat_id=chat_id, text=get_define_data(user, requestText))
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
           ', I\'m afraid you must provide a word for me to define. Like this: /define word')

def get_define_data(user, requestText):
    defineUrl = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    req = urllib2.Request(defineUrl + requestText)
    try:
        tryOpenUrl = urllib2.urlopen(req)
    except HTTPError:
        return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
           ', I\'m afraid I cannot find a defnition for ' + requestText + '.'
    defineData = json.load(tryOpenUrl)
    returnData = ''
    length = len(defineData)
    if length > 0:
        returnData = returnData + '\n*' + defineData[0]['word'].upper() + ':*'
        if 'meanings' in defineData[0] and len(defineData[0]['meanings']) > 0:
            definitionData = ''
            synonymData = '`'
            for j in range(len(defineData[0]['meanings'])):
                if 'definitions' in defineData[0]['meanings'][j] and len(defineData[0]['meanings'][j]['definitions']) > 0:
                    for k in range(len(defineData[0]['meanings'][j]['definitions'])):
                        if 'definition' in defineData[0]['meanings'][j]['definitions'][k]:
                            definitionData = definitionData + ' ' + defineData[0]['meanings'][j]['definitions'][k]['definition']
                        if 'synonyms' in defineData[0]['meanings'][j]['definitions'][k] and len(defineData[0]['meanings'][j]['definitions'][k]['synonyms']) > 0:
                            for l in range(len(defineData[0]['meanings'][j]['definitions'][k]['synonyms'])):
                                synonymData = synonymData + (', ' if synonymData != '`' else '') + defineData[0]['meanings'][j]['definitions'][k]['synonyms'][l]
            synonymData = (synonymData[:1000] + '...') if len(synonymData) > 1000 else synonymData
            synonymData = synonymData + '`'
            definitionData = (definitionData[:1000] + '...') if len(definitionData) > 1000 else definitionData
            definitionData = definitionData.lstrip(' ')
        returnData = returnData + '\n' + definitionData
        if synonymData != '``':
            returnData = returnData + '\n' + synonymData
        if 'phonetics' in defineData[0] and len(defineData[0]['phonetics']) > 0 and 'audio' in defineData[0]['phonetics'][0]:
            returnData = returnData + '\nhttp:' + defineData[0]['phonetics'][0]['audio'].replace('_','\_')
    else:
        return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
           ', I\'m afraid I cannot find a defnition for ' + requestText + '.'
    return returnData
