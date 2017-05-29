# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, chat_id, user, keyConfig='', requestText='', totalResults=1):
    rawAudioSourceTag, error, full_url = search_pronounciations(requestText)
    if rawAudioSourceTag:
        bot.sendMessage(chat_id=chat_id, text='http:' + rawAudioSourceTag)
    else:
        if error and error.text:
            bot.sendMessage(chat_id=chat_id, text='Es tut mir Leid ' + (user if not user == '' else 'Dave') +
                                                  ', ' + error.text + '\n' + full_url)
        else:
            bot.sendMessage(chat_id=chat_id, text='Es tut mir Leid ' + (user if not user == '' else 'Dave') + \
                                                  ', Ich habe angst, dass ich keine aussprache von finden kann ' + \
                                                  requestText.encode('utf-8') + '.\n' + full_url)


def search_pronounciations(requestText):
    rawAudioSourceTag, error, full_url = search_impl(requestText.lower())
    if rawAudioSourceTag:
        return rawAudioSourceTag, error, full_url
    else:
        rawAudioSourceTag, error, full_url = search_impl(requestText.title())
        return rawAudioSourceTag, error, full_url


def search_impl(requestText):
    args = {'from': 'wb',
            'q': requestText}
    full_url = 'https://www.dwds.de/' + '?' + urllib.urlencode(args)
    rawMarkup = urllib.urlopen(full_url).read()
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    getAudioTag = soup.find('source', attrs={'type': 'audio/mpeg'})
    rawAudioSourceTag = getAudioTag['src'] if getAudioTag else None
    error = soup.find('p', attrs={'class': 'bg-danger'})
    return rawAudioSourceTag, error, full_url

