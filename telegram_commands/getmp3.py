# coding=utf-8
import json
import urllib
import string
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import telegram_commands.getvid as getvid

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
    while (offset_this_page < results_this_page):
        vidlink = str(data['items'][offset_this_page]['id']['videoId'])
        offset_this_page += 1
        if is_valid_video(vidlink, chat_id):
            bot.sendMessage(chat_id=chat_id, text='https://youtube2mp3api.com/@api/button/mp3/' + vidlink)
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
    if video_url != '' and not wasPreviouslySeenVideo(video_url, chat_id):
        return True
    return False
