# coding=utf-8
import json
import urllib


def run(user, message, chat_id='', totalResults=1):
    requestText = str(message).strip()

    movieUrl = 'http://www.omdbapi.com/?apikey=' + keyConfig.get('OMDB', 'KEY') + '&plot=short&r=json&y=&t='
    realUrl = movieUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if 'Error' not in data:
        result = (user + ', ' if not user == '' else '') + data['Title'] + ':\n' + data['Plot']
        if 'Poster' in data and not data['Poster'] == 'N/A':
            result += '\n' + data['Poster'].encode('utf-8')
        return result
    else:
        return 'I\'m sorry ' + (
        user if not user == '' else 'Dave') + ', I\'m afraid I can\'t find any movies for ' + \
               requestText.encode('utf-8') + '.'