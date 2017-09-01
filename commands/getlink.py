# coding=utf-8
import json
import string
import urllib
from google.appengine.ext import ndb


class SeenUrls(ndb.Model):
    # key name: get:str(chat_id)
    allPreviousSeenBooks = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenUrlsValue(chat_id, NewValue):
    es = SeenUrls.get_or_insert(str(chat_id))
    es.allPreviousSeenBooks = NewValue.encode('utf-8')
    es.put()

def addPreviouslySeenUrlsValue(chat_id, NewValue):
    es = SeenUrls.get_or_insert(str(chat_id))
    if es.allPreviousSeenBooks == '':
        es.allPreviousSeenBooks = NewValue.encode('utf-8').replace(',', '')
    else:
        es.allPreviousSeenBooks += ',' + NewValue.encode('utf-8').replace(',', '')
    es.put()

def getPreviouslySeenUrlsValue(chat_id):
    es = SeenUrls.get_or_insert(str(chat_id))
    if es:
        return es.allPreviousSeenBooks.encode('utf-8')
    return ''

def wasPreviouslySeenUrl(chat_id, url):
    url = url.replace(',', '')
    allPreviousLinks = getPreviouslySeenUrlsValue(chat_id)
    if ',' + url + ',' in allPreviousLinks or \
            allPreviousLinks.startswith(url + ',') or  \
            allPreviousLinks.endswith(',' + url) or  \
            allPreviousLinks == url:
        return True
    return False

def run(bot, chat_id, user, keyConfig, message, total_requested_results=1):
    requestText = message.replace(bot.name, "").strip()
    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
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
            if not wasPreviouslySeenUrl(chat_id, link):
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


