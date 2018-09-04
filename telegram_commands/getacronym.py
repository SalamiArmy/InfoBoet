# coding=utf-8
import urllib

from bs4 import BeautifulSoup


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, '').strip().upper()

    code = urllib.urlopen('http://www.abbreviations.com/' + requestText).read()
    resultsList = acronym_results_parser(code)
    result = ''
    if resultsList:
        searchResults = acronym_results_printer(requestText, resultsList)
        result = user + ', ' + searchResults
    else:
        result='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I\'m afraid I can\'t find the acronym *' + \
                                              str(requestText) + '*'
    try:
        bot.sendMessage(chat_id=chat_id, text=result, parse_mode='Markdown')
    except:
        bot.sendMessage(chat_id=chat_id, text=result)


def acronym_results_parser(code):
    soup = BeautifulSoup(code, 'html.parser')
    resultList = []
    for resultRow in soup.findAll('p', attrs={'class':'desc'}):
        resultList.append(resultRow.string)
    return resultList

def acronym_results_printer(request, list):
    AllGameDetailsFormatted = '*' + str(request) + '* could mean:'
    for item in list:
        encodedItem = item.encode('utf-8')
        if (encodedItem != 'None'):
            AllGameDetailsFormatted += '\n'
            for char in encodedItem.replace('Definition', '').replace('*', '\*'):
                if char.isupper():
                    AllGameDetailsFormatted += '*' + char + '*'
                else:
                    AllGameDetailsFormatted += char
    return AllGameDetailsFormatted
