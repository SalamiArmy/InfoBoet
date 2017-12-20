# coding=utf-8
import json

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message="", totalResults=1):
    priceGB, priceUS, priceZA, updateTime = get_bitcoin_prices()
    bot.sendMessage(chat_id=chat_id,
                    text='The Current Price of 1 Bitcoin:\n\n' + priceUS +
                         ' USD\n' + priceGB +
                         ' GBP\n' + priceZA + ' ZAR' + '\n\nTime Updated: ' + updateTime)
    return True


def get_bitcoin_prices():
    bcurl = 'https://api.coindesk.com/v1/bpi/currentprice/ZAR.json'
    RAW_DATA = urlfetch.fetch(bcurl)
    if RAW_DATA and RAW_DATA.content:
        data = json.loads(RAW_DATA.content)
        bcurl2 = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        RAW_DATA2 = urlfetch.fetch(bcurl2)
        if RAW_DATA and RAW_DATA2.content:
            try:
                data2 = json.loads(RAW_DATA2.content)
                updateTime = data['time']['updated']
                priceUS = data['bpi']['USD']['rate']
                priceZA = data['bpi']['ZAR']['rate']
                priceGB = data2['bpi']['GBP']['rate']
                return priceGB, priceUS, priceZA, updateTime
            except ValueError:
                print('Value error: ' + RAW_DATA2.content)
        else:
            print('raw bitcoin 2 data returned nothing.')
    else:
        print('raw bitcoin data returned nothing.')
