# coding=utf-8
import json
import urllib


def run(keyConfig, message, totalResults=1):
    requestText = str(message).strip()

    wikiUrl = \
        'https://simple.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&search='
    realUrl = wikiUrl + str(requestText)
    data = json.load(urllib.urlopen(realUrl))
    total_sent = 0
    result = ''
    while len(data) > 2 and int(total_sent) < len(data[2]) and int(total_sent) < int(totalResults):
        result += ('\n' if result != '' else '') + (user + ': ' if not user == '' else '') + \
                  data[2][total_sent] + '\nLink: ' + data[3][total_sent]
        total_sent += 1
    if result == '':
        wikiUrl = \
            'https://en.wikipedia.org/w/api.php?action=opensearch&namespace=0&format=json&search='
        realUrl = wikiUrl + str(requestText)
        data = json.load(urllib.urlopen(realUrl))
        while len(data) > 2 and int(total_sent) < len(data[2]) and int(total_sent) < int(totalResults):
            result += ('\n' if result != '' else '') + (user + ': ' if not user == '' else '') + \
                      data[2][total_sent] + '\nLink: ' + data[3][total_sent]
            total_sent += 1
        if result == '':
            result = 'I\'m sorry Dave, I\'m afraid I can\'t find any wiki articles for ' +\
                     str(requestText) + '.'
    return result
