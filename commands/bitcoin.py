# coding=utf-8
import json

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message="BTC", totalResults=1):
    bcurl = 'https://min-api.cryptocompare.com/data/price?fsym=' + message + '&tsyms=ZAR,USD,EUR'
    RAW_DATA = urlfetch.fetch(bcurl)
    data = json.loads(RAW_DATA.content)
    bot.sendMessage(chat_id=chat_id,
                    text='The Current Price of 1 ' + ticker + ':\n\n' + str(data['USD']) +
                         ' USD\n' + str(data['EUR']) +
                         ' EUR\n' + str(data['ZAR']) + ' ZAR')
    return True
        
