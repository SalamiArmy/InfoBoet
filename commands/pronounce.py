# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, chat_id, user, keyConfig='', requestText='', totalResults=1):
    rawMarkup = urllib.urlopen('https://www.dwds.de/?from=wb&q=' + requestText).read()
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    rawAudioSourceTag = soup.find('source', attrs={'type':'audio/mpeg'})
    if rawAudioSourceTag:
        bot.sendMessage(chat_id=chat_id, text='http:' + rawAudioSourceTag['src'])
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find any pronunciations for ' + \
                                              requestText.encode('utf-8'))

