# coding=utf-8
import json
import random
import string
import urllib


def run(user, message, chat_id='', totalResults=1):
    requestText = str(message).strip()

    dicurl = 'http://api.urbandictionary.com/v0/define?term='
    realUrl = dicurl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if 'list' in data and len(data['list']) >= 1:
        resultNum = data['list'][random.randint(0, len(data['list']) - 1)]
        result = (user + ': ' if not user == '' else '') + 'Urban Definition For ' + string.capwords(
            requestText.encode('utf-8')) + ':\n' + resultNum['definition'] + '\n\nExample:\n' + resultNum['example']
        return result
    else:
        result = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                 ', I\'m afraid I can\'t find any urban definitions for ' + string.capwords(
            requestText.encode('utf-8')) + '.'
        return result
