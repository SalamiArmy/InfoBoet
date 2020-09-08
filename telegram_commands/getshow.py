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
    image_original = ''
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
        if 'image' in data[0]['show'] and data[0]['show']['image'] is not None:
            image_original = str(data[0]['show']['image']['original'])
        result = (user if not user == '' else 'Dave') + ', ' + fullShowDetails + '\n' + formattedShowSummary
    else:
        result = 'I\'m sorry ' + str(user if not user == '' else 'Dave') + \
                 ', I\'m afraid I cannot find the TV show ' + \
                 str(requestText)
    if image_original != '':
        bot.sendPhoto(chat_id=chat_id, photo=image_original)
    try:
        bot.sendMessage(chat_id=chat_id, text=result, parse_mode='Markdown')
    except:
        bot.sendMessage(chat_id=chat_id, text=result)


def parse_show_details(data):
    fullShowDetails = str(data['name']) + ' Is ' + \
                      ('An' if data['status'][0] in ['A', 'E', 'I', 'O', 'U'] else 'A') + ' ' + \
                      str(data['status']) + ' ' + \
                      str(data['type']) + ' ' + \
                      ', '.join(data['genres'])
    if data['premiered'] != None:
        fullShowDetails += '\nPremiere: ' + str(data['premiered'])
    showSchedule = ', '.join(['{0}s'.format(day) for day in data['schedule']['days']]) + \
                   (' at ' + str(data['schedule']['time']) if str(data['schedule']['time']) != '' else '')
    fullShowDetails += '\nRuntime: ' + str(data['runtime']) + ' mins' + \
                       (' ' + showSchedule if showSchedule != '' else '')
    if 'officialSite' in data and data['officialSite'] is not None:
        fullShowDetails += '\n' + str(data['officialSite'])
    return fullShowDetails
