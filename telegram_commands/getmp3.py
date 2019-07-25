# coding=utf-8
import json
import urllib
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import pafy

import main
getvid = main.get_platform_command_code('telegram', 'getvid')

class WhosHeardMP3Urls(ndb.Model):
    # key name: MP3Url
    whoseHeardMP3 = ndb.StringProperty(indexed=False, default='')
    
def addPreviouslyHeardMP3sValue(video_url, chat_id):
    es = WhosHeardMP3Urls.get_or_insert(video_url)
    if es.whoseHeardMP3 == '':
        es.whoseHeardMP3 = str(chat_id)
    else:
        es.whoseHeardMP3 += ',' + str(chat_id)
    es.put()
    
def getwhoseHeardMP3sValue(video_link):
    es = WhosHeardMP3Urls.get_or_insert(video_link)
    if es:
        return str(es.whoseHeardMP3)
    return ''

def wasPreviouslyHeardMP3(video_link, chat_id):
    allWhoveHeardMP3 = getwhoseHeardMP3sValue(video_link)
    if ',' + str(chat_id) + ',' in allWhoveHeardMP3 or \
            allWhoveHeardMP3.startswith(str(chat_id) + ',') or \
            allWhoveHeardMP3.endswith(',' + str(chat_id)) or \
                    allWhoveHeardMP3 == str(chat_id):
        return True
    addPreviouslyHeardMP3sValue(video_link, chat_id)
    return False

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).replace(bot.name, "").strip()
    args = {'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'type': 'video',
            'safeSearch': 'none',
            'q': requestText,
            'part': 'snippet',
            'maxResults': 25}
    data, total_results, results_this_page = Google_Custom_Search(args)
    offset_this_page = 0
    while offset_this_page < results_this_page:
        vidlink = str(data['items'][offset_this_page]['id']['videoId'])
        vidtitle = str(data['items'][offset_this_page]['snippet']['title'])
        viddescription = str(data['items'][offset_this_page]['snippet']['description'])
        offset_this_page += 1
        if is_valid_video(vidlink, chat_id):
            streams = pafy.new("https://www.youtube.com/watch?v=" + vidlink, basic=True).streams
            results = ''
            for s in streams:
                results += s.resolution + ', ' + s.extension + ': ' + s.url + '\n'
            bot.sendMessage(chat_id=chat_id,
                            text=(user if not user == '' else 'Dave') +
                                 ', *' + vidtitle + '*, ' + viddescription + results,
                            parse_mode='Markdown')
            return

def Google_Custom_Search(args):
    googurl = 'https://www.googleapis.com/youtube/v3/search'
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.loads(urlfetch.fetch(realUrl).content)
    total_results = 0
    results_this_page = 0
    if 'pageInfo' in data and 'totalResults' in data['pageInfo']:
        total_results = data['pageInfo']['totalResults']
    if 'items' in data and len(data['items']) > 0:
        results_this_page = len(data['items'])
    return data, total_results, results_this_page

def is_valid_video(video_url, chat_id):
    if video_url != '' and not wasPreviouslyHeardMP3(video_url, chat_id):
        return True
    return False
