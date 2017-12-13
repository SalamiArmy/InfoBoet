# coding=utf-8
import ConfigParser
import json
import string
import urllib
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

CommandName = 'getlink'

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

def run(user, message, chat_id='', total_requested_results=1):
    requestText = str(message).strip()
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    args = {'cx': keyConfig.get('Google', 'GCSE_OTHER_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': "off",
            'q': requestText}
    return Send_Links(chat_id, user, requestText, args, keyConfig, total_requested_results)

def Google_Custom_Search(args):
    googurl = 'https://www.googleapis.com/customsearch/v1'
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.loads(urlfetch.fetch(realUrl).content)
    total_results = 0
    results_this_page = 0
    if 'searchInformation' in data and 'totalResults' in data['searchInformation']:
        total_results = data['searchInformation']['totalResults']
    if 'queries' in data and 'request' in data['queries'] and len(data['queries']['request']) > 0 and 'count' in \
            data['queries']['request'][0]:
        results_this_page = data['queries']['request'][0]['count']
    return data, total_results, results_this_page

def Send_Links(chat_id, user, requestText, args, keyConfig, total_number_to_send=1):
    data, total_results, results_this_page = Google_Custom_Search(args)
    if 'items' in data and total_results > 0:
        total_offset, total_results, total_sent = search_results_walker(args, chat_id, data, total_number_to_send,
                                                                        user + ', ' + requestText, results_this_page,
                                                                        total_results, keyConfig)
        if len(total_sent.split(', ')) < int(total_number_to_send):
            if int(total_number_to_send) > 1:
                return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                                      ', I\'m afraid I can\'t find any more images for ' +\
                                                      string.capwords(requestText.encode('utf-8') + '.' +
                                                                      ' I could only find ' + str(
                                                          len(total_sent.split('\n'))) + ' out of ' + str(total_number_to_send))
            else:
                return 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                                      ', I\'m afraid I can\'t find any images for ' +\
                                                      string.capwords(requestText.encode('utf-8'))
        return total_sent
    else:
        if 'error' in data:
            errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                       data['error']['message']
            return errorMsg
        else:
            errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                       ', I\'m afraid I can\'t find any images for ' + \
                       string.capwords(requestText.encode('utf-8'))
            return errorMsg

def search_results_walker(args, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                          total_offset=0, total_sent=''):
    offset_this_page = 0
    if number != 1:
        total_sent = str(number) + ' ' + requestText + ' links:\n'
    while (total_sent == '' or len(total_sent.split(', ')) < int(number)) and int(offset_this_page) < int(results_this_page):
        link = str(data['items'][offset_this_page]['link'])
        offset_this_page += 1
        total_offset = int(total_offset) + 1
        if not wasPreviouslySeenImage(link, chat_id):
            if number == 1:
                total_sent = requestText + ': ' + link
            else:
                total_sent += (', ' if total_sent[-1:] != '\n' else '') + link
    if (total_sent == '' or len(total_sent.split(', ')) < int(number)) and int(total_offset) < int(total_results):
        args['start'] = total_offset + 1
        data, total_results, results_this_page = Google_Custom_Search(args)
        return search_results_walker(args, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                                     total_offset, total_sent)
    return total_offset, total_results, total_sent
