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
    try:
        tryOpenUrl = urllib2.urlopen(req)
    except HTTPError:
        return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
           ', I\'m afraid I cannot find a defnition for ' + requestText + '.'
    defineData = json.load(tryOpenUrl)
    returnData = ''
    length = len(defineData)
    if length > 0:
        for i in range(length):
            returnData = returnData + '\n*' + defineData[i]['word'].upper() + ':*'
            if 'meanings' in defineData[i] and len(defineData[i]['meanings']) > 0:
                definitionData = ''
                synonymData = '`'
                for j in range(len(defineData[i]['meanings'])):
                    if 'definitions' in defineData[i]['meanings'][j] and len(defineData[i]['meanings'][j]['definitions']) > 0:
                        for k in range(len(defineData[i]['meanings'][j]['definitions'])):
                            if 'definition' in defineData[i]['meanings'][j]['definitions'][k]:
                                definitionData = definitionData + ' ' + defineData[i]['meanings'][j]['definitions'][k]['definition']
                            if 'synonyms' in defineData[i]['meanings'][j]['definitions'][k] and len(defineData[i]['meanings'][j]['definitions'][k]['synonyms']) > 0:
                                for l in range(len(defineData[i]['meanings'][j]['definitions'][k]['synonyms'])):
                                    synonymData = synonymData + (', ' if synonymData != '`' else '') + defineData[i]['meanings'][j]['definitions'][k]['synonyms'][l]
                synonymData = synonymData + '`'
                definitionData = definitionData.lstrip(' ')
            returnData = returnData + '\n' + definitionData
            if synonymData != '``':
                returnData = returnData + '\n' + synonymData
            if 'phonetics' in defineData[i] and len(defineData[i]['phonetics']) > 0:
                returnData = returnData + '\nhttp:' + defineData[i]['phonetics'][0]['audio'].replace('_','\_')
    return returnData
