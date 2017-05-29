# coding=utf-8
import json
import urllib

import telegram
from bs4 import BeautifulSoup


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    airportCode = get_airport_code(requestText)
    if airportCode != 'No matching entries found...':
        bot.sendMessage(chat_id=chat_id, text=airportCode)
        return True
    else:
        bot.sendMessage(chat_id=chat_id,
                        text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                             ', I\'m afraid I can\'t quite place ' + requestText.encode('utf-8') + '.')


def get_airport_code(cityName):
    airportsUrl = 'http://www.webflyer.com/travel/milemarker/getmileage_ft.cgi?city='
    realUrl = airportsUrl + cityName.encode('utf-8')
    code = urllib.urlopen(realUrl).read()
    data = BeautifulSoup(code, 'html.parser')
    error = data.find('b').string
    airportCode = str(data.findAll('b')[1]) if error != 'No matching entries found...' else ''
    return error.replace('Here are the results of your search:', ''), airportCode