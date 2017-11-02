# coding=utf-8
import json
import string
import urllib
from google.appengine.ext import ndb

class WhoseSeenUrls(ndb.Model):
    # key name: get:str(chat_id)
    whoseSeen = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenUrlsValue(url, NewValue):
    es = WhoseSeenUrls.get_or_insert(str(url))
    es.whoseSeen = str(NewValue)
    es.put()

def addPreviouslySeenUrlsValue(url, chat_id):
    es = WhoseSeenUrls.get_or_insert(url)
    if es.whoseSeen == '':
        es.whoseSeen = str(chat_id)
    else:
        es.whoseSeen += ',' + str(chat_id)
    es.put()

def getwhoseSeensValue(image_link):
    print image_link
    es = WhoseSeenUrls.get_or_insert(image_link)
    if es:
        return str(es.whoseSeen)
    return ''

def wasPreviouslySeenImage(image_link, chat_id):
    all_whove_seen_url = getwhoseSeensValue(image_link)
    if ',' + str(chat_id) + ',' in all_whove_seen_url or \
            all_whove_seen_url.startswith(str(chat_id) + ',') or \
            all_whove_seen_url.endswith(',' + str(chat_id)) or \
                    all_whove_seen_url == str(chat_id):
        return True
    addPreviouslySeenUrlsValue(image_link, chat_id)
    return False

def run(bot, chat_id, user, keyConfig, message, total_requested_results=1):
    requestText = message.replace(bot.name, "").strip()
    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig.get('Google', 'GCSE_OTHER_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': "off",
            'q': requestText}
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.load(urllib.urlopen(realUrl))
    if 'items' in data:
        total_sent = 0
        total_actual_results = int(data['searchInformation']['totalResults'])
        if int(total_actual_results) < int(total_requested_results):
            total_results_to_send = int(total_actual_results)
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can only find ' + str(total_actual_results) +
                                                  ' links for ' + string.capwords(requestText.encode('utf-8')) + '.')
        else:
            total_results_to_send = int(total_requested_results)
        while total_sent < total_results_to_send:
            link = data['items'][total_sent]['link']
            if not wasPreviouslySeenImage(link, chat_id):
                bot.sendMessage(chat_id=chat_id, text=user + ', ' + requestText +
                                                      (' ' + str(total_sent + 1) + ' of ' + str(total_results_to_send) if int(total_results_to_send) > 1 else '') +
                                                      ': ' + link)
                total_sent += 1
                addPreviouslySeenUrlsValue(chat_id, link)
    else:
        if 'error' in data:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ' I got ' + data['error']['message'] + '.')
        else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any links for ' +
                                                  string.capwords(requestText.encode('utf-8')))


