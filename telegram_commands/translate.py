# coding=utf-8
import ConfigParser
import json
import logging
try:
    from urllib.parse import urlparse
    from urllib.request import urlopen
except ImportError:
    # For Python 2
    from urlparse import urlparse
    from urllib2 import urlopen


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    translateUrl = 'https://www.googleapis.com/language/translate/v2?key=' + \
                   keyConfig.get('Google', 'GCSE_APP_ID') + '&target=en&q='
    realUrl = translateUrl + requestText
    if is_valid_url(realUrl):
        data = json.load(urlopen(realUrl))
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
                result = (user + ': ' if not user == '' else '') + \
                                                      'Detected language: ' + detectedLanguageSemanticName + \
                                                      '\nMeaning: ' + translation\
                                .replace('&#39;', '\'')\
                                .replace('&quot;', '"') + '.'
            else:
                result = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                      ', I\'m afraid I can\'t find any translations for ' + \
                                                      requestText.encode('utf-8') + '.'
        else:
            if 'error' in data and 'message' in data['error']:
                result = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                       ', ' + data['error']['message']
            else:
                result = 'Cannot parse ' + str(data)
        bot.sendMessage(chat_id=chat_id, text=result)
    else:
        bot.sendMessage(chat_id=chat_id, text="Request contains invalid charcters")

def is_valid_url(url):
    try:
        # Parse the URL
        parsed_url = urlparse(url)

        # Check if the scheme and netloc are present
        if parsed_url.scheme and parsed_url.netloc:
            return True
        else:
            return False
    except ValueError:
        return False
