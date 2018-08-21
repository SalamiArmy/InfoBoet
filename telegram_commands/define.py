# coding=utf-8
import ConfigParser
import json
import urllib
import urllib2

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])
    if requestText != '':
        bot.sendMessage(chat_id=chat_id, text=get_define_data(keyConfig, user, requestText))
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
           ', I\'m afraid you must provide a word for me to define. Like this: /define word')

def get_define_data(keyConfig, user, requestText):
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
            if 'results' in data and len(data['results']) > 0 and 'lexicalEntries' in data['results'][0] and len(data['results'][0]['lexicalEntries']) > 0 and 'entries' in data['results'][0]['lexicalEntries'][0] and len(data['results'][0]['lexicalEntries'][0]['entries']) > 0 and 'audioFile' in data['results'][0]['lexicalEntries'][0]['entries'][0]:
                pronounce = data['results'][0]['lexicalEntries'][0]['pronunciations'][0]['audioFile']
            definition = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
            synonymsReq = urllib2.Request(definitionUrl + formatted_entry.lower() + '/synonyms')
            synonymsReq.add_header('app_id', keyConfig.get('OxfordDictionaries', 'ID'))
            synonymsReq.add_header('app_key', keyConfig.get('OxfordDictionaries', 'KEY'))
            try:
                synonymsData = json.load(urllib2.urlopen(synonymsReq))
            except urllib2.HTTPError:
                print('HTTP Error for Synonyms: ' + definitionUrl + formatted_entry.lower())
            synonyms = ''
            if 'results' in synonymsData and len(synonymsData['results']) > 0 and 'lexicalEntries' in synonymsData['results'][0] and len(synonymsData['results'][0]['lexicalEntries']) > 0 and 'entries' in synonymsData['results'][0]['lexicalEntries'][0] and len(synonymsData['results'][0]['lexicalEntries'][0]['entries']) > 0 and 'senses' in synonymsData['results'][0]['lexicalEntries'][0]['entries'][0] and len(synonymsData['results'][0]['lexicalEntries'][0]['entries'][0]['senses']) > 0 and 'synonyms' in synonymsData['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0] and len(synonymsData['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']) > 0:
                synonyms = ', '.join(o['text'] for o in synonymsData['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms'])
            return (user if not user == '' else 'Dave') + ', ' + formatted_entry + ': ' + definition + ('\n' + pronounce if not pronounce == '' else '') + ('\n' + synonyms if not synonyms == '' else '')
    return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
           ', I\'m afraid I can\'t find any definitions for the word ' + requestText
