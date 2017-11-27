# coding=utf-8
import json
import re
import urllib


def run(user, message, chat_id='', totalResults=1):
    requestText = str(message).strip()

    data = wiki_search('%22' + requestText + '%22')
    if len(data['query']['search']) >= 1:
        return (user + ': ' if not user == '' else '') + data['query']['search'][0]['snippet'] +\
               '\nhttps://en.wikiquote.org/wiki/' +\
               urllib.quote(data['query']['search'][0]['title'].encode('utf-8'))
    else:
        data = wiki_search(requestText)
        if len(data['query']['search']) >= 1:
            return (user + ': ' if not user == '' else '') + data['query']['search'][0]['snippet'] +\
           '\nhttps://en.wikiquote.org/wiki/' +\
           urllib.quote(data['query']['search'][0]['title'].encode('utf-8'))
        else:
            return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                   ', I\'m afraid I can\'t find any quotes for ' +\
                   requestText.encode('utf-8') + '.'


def wiki_search(requestText):
    wikiUrl = \
        'https://en.wikiquote.org/w/api.php?action=query&list=search&srlimit=1&namespace=0&format=json&srsearch='
    realUrl = wikiUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    return data