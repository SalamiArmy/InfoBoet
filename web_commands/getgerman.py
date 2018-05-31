# coding=utf-8
import json
import urllib


def run(keyConfig, message, totalResults=1):
    requestText = message.strip()

    translateUrl = 'https://www.googleapis.com/language/translate/v2?key=' + \
                   keyConfig.get('Google', 'GCSE_APP_ID') + '&target=de&q='
    realUrl = translateUrl + requestText.encode('utf-8')
    data = json.load(urllib.urlopen(realUrl))
    if len(data['data']['translations']) >= 1:
        translation = data['data']['translations'][0]['translatedText']
        return 'in German: ' + translation
    else:
        return 'I\'m sorry Dave, I\'m afraid I can\'t find any translations for ' + str(requestText) + '.'