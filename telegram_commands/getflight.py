# coding=utf-8
import urllib

from bs4 import BeautifulSoup


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    if (requestText[3] == " " and requestText[7] == " " and requestText[12] == "-" and requestText[15] == "-" and requestText[18] == " " and requestText[23] == "-" and requestText[26] == "-"):
        bot.sendMessage(chat_id=chat_id, text=get_returnflights(requestText), disable_web_page_preview=True)
        return True
    else:
        if (requestText[3] == " " and requestText[7] == " " and requestText[12] == "-" and requestText[15] == "-"):
            bot.sendMessage(chat_id=chat_id, text=get_flights(requestText), disable_web_page_preview=True)
            return True
        else:
            airportCode, error = get_airport_code(requestText)
            if airportCode != '':
                bot.sendMessage(chat_id=chat_id, text=airportCode)
                return True
            else:
                if error:
                    bot.sendMessage(chat_id=chat_id,
                                    text='I\'m sorry ' + (user if not user == '' else 'Dave') + ', ' +
                                         error)
                else:
                    bot.sendMessage(chat_id=chat_id,
                                    text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                         ', I\'m afraid I can\'t quite place ' + requestText.encode('utf-8') + '.')
    bot.sendMessage(chat_id=chat_id,
                    text='This bot has three modes:\nAirport code search, for example \'/getflight lucerne\' request returns \'QLJ\'.\nOne-way flight search, for example \'/getflight DUR DUB 1988-06-28\' request returns a link to a list of flights.\nRound-trip search for example \'\getflight DUR DUB 1988-06-28 1988-07-17\' request returns a link to a list of flights with a return flight on 1988-07-17.')



def get_airport_code(cityName):
    airportsUrl = 'http://www.webflyer.com/travel/milemarker/getmileage_ft.cgi?city='
    realUrl = airportsUrl + cityName.encode('utf-8')
    code = urllib.urlopen(realUrl).read()
    data = BeautifulSoup(code, 'html.parser')
    error = data.find('b').string
    rawAirportCode = str(data.findAll('b')[1]) if error != 'No matching entries found...' else ''
    airportCode = rawAirportCode[4:rawAirportCode.index(')<br/>')] if len(rawAirportCode) > 13 else ''
    return airportCode, error.replace('Here are the results of your search:', '')

def get_flights(requestText):
    return 'https://www.google.co.uk/flights/?gl=ie#flt=' + requestText.replace(' ', '.') + ';c:EUR;e:1;sd:1;t:f;tt:o'

def get_returnflights(requestText):
    requestParts = requestText.split(' ')
    parsedRequest = requestParts[0] + '.' + requestParts[1] + '.' + requestParts[2] + '*' + requestParts[1] + '.' + requestParts[0] + '.' + requestParts[3]
    return 'https://www.google.co.uk/flights/?gl=ie#flt=' + parsedRequest + ';c:EUR;e:1;sd:1;t:f'
