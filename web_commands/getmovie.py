# coding=utf-8
import ConfigParser
import json
import urllib


def run(keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    movieUrl = 'http://www.omdbapi.com/?apikey=' + keyConfig.get('OMDB', 'KEY') + '&plot=short&r=json&y=&t='
    realUrl = movieUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if 'Error' not in data:
        result = data['Title'] + ':\n' + data['Plot']
        if 'Poster' in data and not data['Poster'] == 'N/A':
            result += '\n' + data['Poster'].encode('utf-8')
    else:
        result = 'I\'m sorry Dave, I\'m afraid I can\'t find any movies for ' + str(requestText) + '.'
    return result