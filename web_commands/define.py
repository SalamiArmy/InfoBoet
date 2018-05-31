# coding=utf-8
import ConfigParser
import json
import urllib
import urllib2

def run(keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])
    if requestText != '':
        return get_define_data(keyConfig, requestText)
    else:
        return 'I\'m sorry Dave, I\'m afraid you must provide a word for me to define. Like this: /define word'

def get_define_data(keyConfig, requestText):
    spellingUrl = 'https://od-api.oxforddictionaries.com/api/v1/search/en'
    values = {'q': requestText.lower(), 'prefix':'false'}
    data = urllib.urlencode(values)
    req = urllib2.Request(spellingUrl + '?' + data)
    req.add_header('app_id', keyConfig.get('OxfordDictionaries', 'ID'))
    req.add_header('app_key', keyConfig.get('OxfordDictionaries', 'KEY'))
    spellingData = json.load(urllib2.urlopen(req))
    if 'results' in spellingData and len(spellingData['results']) > 0:
        formatted_entry = spellingData['results'][0]['word']

        definitionUrl = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/'
        req = urllib2.Request(definitionUrl + formatted_entry.lower())
        req.add_header('app_id', keyConfig.get('OxfordDictionaries', 'ID'))
        req.add_header('app_key', keyConfig.get('OxfordDictionaries', 'KEY'))
        try:
            data = json.load(urllib2.urlopen(req))
        except urllib2.HTTPError:
            print('HTTP Error: ' + definitionUrl + formatted_entry.lower())
        if data and 'results' in data and len(data['results']) > 0 and 'lexicalEntries' in data['results'][0] and len(data['results'][0]['lexicalEntries']) > 0 and 'entries' in data['results'][0]['lexicalEntries'][0] and len(data['results'][0]['lexicalEntries'][0]['entries']) > 0 and 'senses' in data['results'][0]['lexicalEntries'][0]['entries'][0] and len(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses']) > 0 and 'definitions' in data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0] and len(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions']) > 0:
            pronounce = ''
            definition = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
            if 'results' in data and len(data['results']) > 0 and 'lexicalEntries' in data['results'][0] and len(data['results'][0]['lexicalEntries']) > 0 and 'pronunciations' in data['results'][0]['lexicalEntries'][0] and len(data['results'][0]['lexicalEntries'][0]['pronunciations']) > 0 and 'audioFile' in data['results'][0]['lexicalEntries'][0]['pronunciations'][0]:
                pronounce = data['results'][0]['lexicalEntries'][0]['pronunciations'][0]['audioFile']
            return 'Dave, ' + formatted_entry + ': ' + definition + ('\n' + pronounce if not pronounce == '' else '')
    return 'I\'m sorry Dave, I\'m afraid I can\'t find any definitions for the word ' + requestText
