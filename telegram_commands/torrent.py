# coding=utf-8
import json
import urllib

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    torrentsSearchText = GetTorrentSearchText(requestText)

    if torrentsSearchText:
        bot.sendMessage(chat_id=chat_id, text='Serial Magent Link:\n' + str(torrentsSearchText))
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I can\'t find any torrents for ' + \
                                              str(requestText) + '.')

def GetTorrentSearchText(text):
    raw_token_data = urlfetch.fetch(
        url='https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=hey+boet',
        headers={'Accept': 'application/json'})
    tokenData = json.loads(raw_token_data.content)
    fetchUrl = 'https://torrentapi.org/pubapi_v2.php?token=' + tokenData['token'] + '&app_id=hey+boet&mode=search&search_string=' + text
    print(fetchUrl)
    raw_data = urlfetch.fetch(
        url=fetchUrl,
        headers={'Accept': 'application/json'})
    torrentData = json.loads(raw_data.content)
    if 'error' not in torrentData and 'torrent_results' in torrentData:
        if len(torrentData['torrent_results']) > 0 and 'download' in torrentData['torrent_results'][0]:
            return str(torrentData['torrent_results'][0]['download'])
        else:
            return ''
    else:
        return str(torrentData) 
