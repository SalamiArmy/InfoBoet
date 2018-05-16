# coding=utf-8
import sys

import logging

reload(sys)
sys.setdefaultencoding('utf8')
import json
import re
import urllib

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).strip()

    showsUrl = 'http://api.tvmaze.com/search/shows?q='
    data = json.load(urllib.urlopen(showsUrl + requestText))
    logging.info('got show data:')
    logging.info(data)
    result = ''
    if len(data) >= 1:
        formattedShowSummary = re.sub(r'<[^>]*?>', '',
                                      str(data[0]['show']['summary'])
                                       .replace('<span class="searchmatch">', '*')
                                       .replace('</span>', '*')
                                       .replace('&quot;', '\"')
                                       .replace('[', '')
                                       .replace(']', '')
                                       .replace('\\', ''))
        fullShowDetails = parse_show_details(data[0]['show'])
        image_original = ''
        if 'image' in data[0]['show'] and data[0]['show']['image'] is not None:
            image_original = data[0]['show']['image']['original'].encode('utf-8')
        result = (user if not user == '' else 'Dave') + ', ' + fullShowDetails + '\n' + \
                  formattedShowSummary + '\n' + image_original
    else:
        result = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                 ', I\'m afraid I cannot find the TV show ' + \
                 requestText.title()
    bot.sendMessage(chat_id=chat_id, text=result)


def parse_show_details(data):
    fullShowDetails = str(data['name']) + ': ' + \
                      ('An' if data['status'][0] in ['A', 'E', 'I', 'O', 'U'] else 'A') + ' ' + \
                      str(data['status']) + ' ' + \
                      str(data['type']) + ' ' + \
                      ', '.join(data['genres'])
    if data['premiered'] != None:
        fullShowDetails += '\nPremiere: ' + data['premiered']
    showSchedule = ', '.join(['{0}s'.format(day) for day in data['schedule']['days']]) + \
                   (' at ' + data['schedule']['time'] if data['schedule']['time'] != '' else '')
    fullShowDetails += '\nRuntime: ' + str(data['runtime']) + ' mins' + \
                       (' ' + showSchedule if showSchedule != '' else '')
    if 'officialSite' in data and data['officialSite'] is not None:
        fullShowDetails += '\n' + data['officialSite']
    return fullShowDetails
