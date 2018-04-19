# coding=utf-8
import json

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message='BTC', totalResults=1):
    if message == '':
        message = 'BTC'
    bcurl = 'https://min-api.cryptocompare.com/data/price?fsym=' + message + '&tsyms=ZAR,USD,EUR'
    RAW_DATA = urlfetch.fetch(bcurl)
    data = json.loads(RAW_DATA.content)
    if 'USD' in data and 'EUR' in data and 'ZAR' in data:
        bot.sendMessage(chat_id=chat_id,
                        text='The Current Price of 1 ' + message + ':\n\n' + str(data['USD']) +
                             ' USD\n' + str(data['EUR']) +
                             ' EUR\n' + str(data['ZAR']) + ' ZAR')
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', ' + data['Message'])
    return True
        
