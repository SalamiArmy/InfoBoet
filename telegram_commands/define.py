# coding=utf-8
import ConfigParser
import json
import urllib
import urllib2

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    if requestText != '':
        bot.sendMessage(chat_id=chat_id, text=get_define_data(user, requestText), parse_mode='Markdown')
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
           ', I\'m afraid you must provide a word for me to define. Like this: /define word')

def get_define_data(user, requestText):
    defineUrl = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    req = urllib2.Request(defineUrl + requestText)
    definitionData = json.load(urllib2.urlopen(req))
    returnData = ''
    length = len(definitionData)
    if length > 0:
        for i in range(length):
            returnData = returnData + '\n*' + definitionData[i]['word'] + ':*'
            if 'meanings' in definitionData[i] and len(definitionData[i]['meanings']) > 0:
                definitionData = ''
                synonymData = '`'
                for j in range(len(definitionData[i]['meanings'])):
                    if 'definitions' in definitionData[i]['meanings'][j] and len(definitionData[i]['meanings'][j]['definitions']) > 0:
                        for k in range(len(definitionData[i]['meanings'][j]['definitions'])):
                            if 'definition' in definitionData[i]['meanings'][j]['definitions'][k]:
                                definitionData = definitionData + ' ' + definitionData[i]['meanings'][j]['definitions'][k]['definition']
                            if 'synonyms' in definitionData[i]['meanings'][j]['definitions'][k] and len(definitionData[i]['meanings'][j]['definitions'][k]['synonyms']) > 0:
                                for l in range(len(definitionData[i]['meanings'][j]['definitions'][k]['synonyms'])):
                                    synonymData = synonymData + ',' + definitionData[i]['meanings'][j]['definitions'][k]['synonyms'][l]
                synonymData = synonymData.lstrip(',') + '`'
                definitionData = definitionData.lstrip(' ')
            returnData = returnData + '\n' + definitionData + '\n' + synonymData
    return returnData
