# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, chat_id, user, keyConfig='', requestText='', totalResults=1):
    rawAudioSourceTag, error = search_pronounciations(requestText)
    if rawAudioSourceTag:
        bot.sendMessage(chat_id=chat_id, text='http:' + rawAudioSourceTag['src'])
    else:
        if error and error.text:
            bot.sendMessage(chat_id=chat_id, text='Es tut mir Leid ' + (user if not user == '' else 'Dave') +
                                                  ', ' + error.text)
        else:
            bot.sendMessage(chat_id=chat_id, text='Es tut mir Leid ' + (user if not user == '' else 'Dave') + \
                                                  ', Ich habe angst, dass ich keine aussprache von finden kann ' + \
                                                  requestText.encode('utf-8') + '.')


def search_pronounciations(requestText, titleCase=True):
    error, rawAudioSourceTag = search_impl(requestText)
    if rawAudioSourceTag:
        return rawAudioSourceTag, error
    else:
        rawAudioSourceTag, error = search_impl(requestText.title())
        return rawAudioSourceTag, error


def search_impl(requestText):
    args = {'from': 'wb',
            'q': requestText}
    full_url = 'https://www.dwds.de/' + '?' + urllib.urlencode(args)
    rawMarkup = urllib.urlopen(full_url).read()
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    rawAudioSourceTag = soup.find('source', attrs={'type': 'audio/mpeg'})
    error = soup.find('p', attrs={'class': 'bg-danger'})
    return error, rawAudioSourceTag

