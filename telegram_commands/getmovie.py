# coding=utf-8
import ConfigParser
import json
import urllib


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    movieUrl = 'http://www.omdbapi.com/?apikey=' + keyConfig.get('OMDB', 'KEY') + '&plot=short&r=json&y=&t='
    realUrl = movieUrl + str(requestText)
    data = json.load(urllib.urlopen(realUrl))
    result = ''
    if 'Error' not in data:
        result = (user + ', ' if not user == '' else '') + data['Title'] + ':\n' + data['Plot']
        if 'Poster' in data and not data['Poster'] == 'N/A':
            result += '\n' + data['Poster'].encode('utf-8')
    else:
        result = 'I\'m sorry ' + (
        user if not user == '' else 'Dave') + ', I\'m afraid I can\'t find any movies for ' + \
               requestText.encode('utf-8') + '.'
    bot.sendMessage(chat_id=chat_id, text=result)