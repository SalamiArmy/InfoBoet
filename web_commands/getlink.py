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
    seen = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setPreviouslySeenUrlsValue(url, NewValue):
    es = WhoseSeenUrls.get_or_insert(str(url))
    es.seen = NewValue
    es.put()

def addPreviouslySeenUrlsValue(url):
    es = WhoseSeenUrls.get_or_insert(url)
    es.seen = True
    es.put()

def getseensValue(image_link):
    es = WhoseSeenUrls.get_or_insert(image_link)
    if es:
        return es.seen
    return False

def wasPreviouslySeenImage(image_link):
    all_whove_seen_url = getseensValue(image_link)
    if all_whove_seen_url.seen:
        return True
    addPreviouslySeenUrlsValue(image_link)
    return False

def run(keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    args = {'cx': keyConfig.get('Google', 'GCSE_OTHER_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': "off",
            'q': requestText}
    return Send_Links(requestText, args, keyConfig, totalResults)

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

def Send_Links(requestText, args, keyConfig, total_number_to_send=1):
    data, total_results, results_this_page = Google_Custom_Search(args)
    if 'items' in data and total_results > 0:
        total_offset, total_results, total_sent = search_results_walker(args, data, total_number_to_send,
                                                                        requestText, results_this_page,
                                                                        total_results, keyConfig)
        if len(total_sent.split(', ')) < int(total_number_to_send):
            if int(total_number_to_send) > 1:
                return 'I\'m sorry Dave' +\
                                                      ', I\'m afraid I can\'t find any more links for ' +\
                                                      string.capwords(requestText.encode('utf-8') + '.' +
                                                                      ' I could only find ' + str(
                                                          len(total_sent.split('\n'))) + ' out of ' + str(total_number_to_send))
            else:
                return 'I\'m sorry Dave' +\
                                                      ', I\'m afraid I can\'t find any links for ' +\
                                                      string.capwords(requestText.encode('utf-8'))
        return total_sent
    else:
        if 'error' in data:
            errorMsg = 'I\'m sorry Dave' +\
                       data['error']['message']
            return errorMsg
        else:
            errorMsg = 'I\'m sorry Dave' + \
                       ', I\'m afraid I can\'t find any links for ' + \
                       string.capwords(requestText.encode('utf-8'))
            return errorMsg

def search_results_walker(args, data, number, requestText, results_this_page, total_results, keyConfig,
                          total_offset=0, total_sent=''):
    offset_this_page = 0
    if number != 1:
        total_sent = requestText + ' ' + str(number) + ' links:\n'
    while (total_sent == '' or len(total_sent.split(', ')) < int(number)) and int(offset_this_page) < int(results_this_page):
        link = str(data['items'][offset_this_page]['link'])
        offset_this_page += 1
        total_offset = int(total_offset) + 1
        if not wasPreviouslySeenImage(link):
            if number == 1:
                total_sent = requestText + ':\n' + link
            else:
                total_sent += (', ' if total_sent[-1:] != '\n' else '') + link
    if (total_sent == '' or len(total_sent.split(', ')) < int(number)) and int(total_offset) < int(total_results):
        args['start'] = total_offset + 1
        data, total_results, results_this_page = Google_Custom_Search(args)
        return search_results_walker(args, data, number, requestText, results_this_page, total_results, keyConfig,
                                     total_offset, total_sent)
    return total_offset, total_results, total_sent
