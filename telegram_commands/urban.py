# coding=utf-8
import json
import random
import string
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).strip()

    dicurl = 'http://api.urbandictionary.com/v0/define?term='
    realUrl = dicurl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if 'list' in data and len(data['list']) >= 1:
        resultNum = data['list'][random.randint(0, len(data['list']) - 1)]
        result = (user + ': ' if not user == '' else '') + \
                 'Urban Definition For ' + str(requestText) + ':\n' + resultNum['definition'] + '\n\nExample:\n' + resultNum['example']
    else:
        result = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                 ', I\'m afraid I can\'t find any urban definitions for ' + str(requestText) + '.'
    bot.sendMessage(chat_id=chat_id, text=result, parse_mode='Markdown')
