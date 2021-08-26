# coding=utf-8
import ConfigParser
import json
import urllib
import urllib2

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    if requestText != '':
        bot.sendMessage(chat_id=chat_id, text=get_define_data(user, requestText))
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
           ', I\'m afraid you must provide a word for me to define. Like this: /define word')

def get_define_data(user, requestText):
    defineUrl = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    req = urllib2.Request(defineUrl + requestText)
    definitionData = json.load(urllib2.urlopen(req))
    returnData = ''
    length = len(definitionData)
    for i in range(length):
        returnData = returnData + '\n' + definitionData[i].dumps()        
    return returnData
