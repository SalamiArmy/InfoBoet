# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
import re
import urllib
import telegram
import main
say = main.load_code_as_module('say')


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).replace(bot.name, "").strip()

    showsUrl = 'http://api.tvmaze.com/search/shows?q='
    data = json.load(urllib.urlopen(showsUrl + requestText))
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
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            image_original = data[0]['show']['image']['original'].encode('utf-8')
            bot.sendPhoto(chat_id=chat_id,
                          photo=image_original)
        bot.sendMessage(chat_id=chat_id,
                        text=(user if not user == '' else 'Dave') + ', ' + fullShowDetails)
        return say.send_text_as_voice(chat_id, keyConfig, formattedShowSummary, 'en-US_LisaVoice')
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I cannot find the TV show ' + 
                                              requestText.title())


def parse_show_details(data):
    fullShowDetails = str(data['name']) + ': ' + \
                      ('An' if data['status'][0] in ['A', 'E', 'I', 'O', 'U'] else 'A') + ' ' + \
                      str(data['status']) + ' ' + \
                      str(data['type']) + ' ' + \
                      ', '.join(data['genres'])
    fullShowDetails += '\nPremiere: ' + data['premiered']
    showSchedule = ', '.join(['{0}s'.format(day) for day in data['schedule']['days']]) + \
                   (' at ' + data['schedule']['time'] if data['schedule']['time'] != '' else '')
    fullShowDetails += '\nRuntime: ' + str(data['runtime']) + ' mins' + \
                       (' ' + showSchedule if showSchedule != '' else '')
    if 'officialSite' in data and data['officialSite'] is not None:
        fullShowDetails += '\n' + data['officialSite']
    return fullShowDetails
