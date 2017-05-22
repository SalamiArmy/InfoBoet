# coding=utf-8
import urllib
import urllib2

from bs4 import BeautifulSoup


def run(bot, chat_id, user, keyConfig='', requestText='', totalResults=1):
    args = {'from': 'wb',
            'q': requestText.title()}
    full_url = 'https://www.dwds.de/' + '?' + urllib.urlencode(args)
    print full_url
    rawMarkup = urllib.urlopen(full_url).read()
    soup = BeautifulSoup(rawMarkup, 'html.parser')
    rawAudioSourceTag = soup.find('source', attrs={'type':'audio/mpeg'})
    if rawAudioSourceTag:
        bot.sendMessage(chat_id=chat_id, text='http:' + rawAudioSourceTag['src'])
    else:
        error = soup.find('p', attrs={'class':'bg-danger'})
        if error:
            bot.sendMessage(chat_id=chat_id, text='Es tut mir Leid ' + (user if not user == '' else 'Dave') +
                                                  ', ' + error.text)
        else:
            bot.sendMessage(chat_id=chat_id, text='Es tut mir Leid ' + (user if not user == '' else 'Dave') + \
                                                  ', Ich habe angst, dass ich keine aussprache von finden kann ' + \
                                                  requestText.encode('utf-8'))

