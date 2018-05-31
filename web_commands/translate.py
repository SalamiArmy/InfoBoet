# coding=utf-8
import ConfigParser
import json
import logging
import urllib


def run(keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    translateUrl = 'https://www.googleapis.com/language/translate/v2?key=' + \
                   keyConfig.get('Google', 'GCSE_APP_ID') + '&target=en&q='
    realUrl = translateUrl + requestText
    data = json.load(urllib.urlopen(realUrl))
    logging.info('response body:')
    logging.info(data)
    if 'data' in data and 'translations' in data['data']:
        if len(data['data']['translations']) >= 1 and data['data']['translations'][0]['translatedText'] != requestText:
            translation = data['data']['translations'][0]['translatedText']
            detectedLanguage = data['data']['translations'][0]['detectedSourceLanguage']
            languagesList = json.load(urllib.urlopen(
                'https://www.googleapis.com/language/translate/v2/languages?target=en&key=' + keyConfig.get(
                    'Google', 'GCSE_APP_ID')))['data']['languages']
            if len([lang for lang in languagesList if lang['language'] == detectedLanguage]) > 0:
                detectedLanguageSemanticName = [lang for lang in languagesList
                                                if lang['language'] == detectedLanguage][0]['name']
            else:
                detectedLanguageSemanticName = ''
            result = 'Detected language: ' + detectedLanguageSemanticName + \
                                                  '\nMeaning: ' + translation\
                            .replace('&#39;', '\'')\
                            .replace('&quot;', '"') + '.'
        else:
            result = 'I\'m sorry Dave' + \
                                                  ', I\'m afraid I can\'t find any translations for ' + \
                                                  requestText.encode('utf-8') + '.'
    else:
        if 'error' in data and 'message' in data['error']:
            result = 'I\'m sorry Dave' +\
                   ', ' + data['error']['message']
        else:
            result = 'Cannot parse ' + str(data)
    return result