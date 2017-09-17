# coding=utf-8
import json
import re
import urllib

import requests
import telegram
import say


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()


    showsUrl = 'http://api.tvmaze.com/search/shows?q='
    data = json.load(urllib.urlopen(showsUrl + requestText))
    if len(data) >= 1:
        formattedShowSummary = re.sub(r'<[^>]*?>', '',
                                      data[0]['show']['summary']
                                       .replace('<span class="searchmatch">', '*')
                                       .replace('</span>', '*')
                                       .replace('&quot;', '\"')
                                       .replace('[', '')
                                       .replace(']', '')
                                       .replace('\\', ''))
        if 'image' in data[0]['show'] and data[0]['show']['image'] is not None:
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            image_original = data[0]['show']['image']['original'].encode('utf-8')
            bot.sendPhoto(chat_id=chat_id,
                          photo=image_original)
        bot.sendMessage(chat_id=chat_id,
                        text=(user if not user == '' else 'Dave') + ', ' + data[0]['show']['name'] + ': ' +
                             formattedShowSummary)
        data = say.get_voice(requestText, keyConfig, 'en-US_LisaVoice')
        if data:
            requests.post('https://api.telegram.org/bot' + keyConfig.get('Telegram', 'TELE_BOT_ID') +
                          '/sendVoice?chat_id='+str(chat_id),
                          files={'voice': ('no but what I\'M saying is.ogg', data, 'audio/ogg', {'Expires': '0'})})
            sent = True
        return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I cannot find the TV show ' + 
                                              requestText.title())