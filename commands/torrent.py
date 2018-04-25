# coding=utf-8
import json
import urllib

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    torrentSearchText = GetTorrentSearchText(requestText, keyConfig)

    if torrentSearchText:
        bot.sendMessage(chat_id=chat_id, text=torrentSearchText)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I can\'t find any torrents for ' + \
                                              requestText.encode('utf-8') + '.')

def GetTorrentSearchText(text, keyConfig):
    raw_data = urlfetch.fetch(
        url='https://oneom.tk/search/serial?limit=1&title=' + text,
        headers={'Accept': 'application/json'})
    torrentData = json.loads(raw_data.content)
    if 'error' not in torrentData and 'serials' in torrentData:
        if len(torrentData['serials']) > 0 and 'id' in torrentData['serials'][0]:
            return GetTorrentMagnetLink(str(torrentData['serials'][0]['id']), keyConfig)
        else:
            return ''
    else:
        return str(torrentData)

def GetTorrentMagnetLink(text, keyConfig):
    raw_data = urlfetch.fetch(
        url='https://oneom.tk/ep/' + text,
        headers={'Accept': 'application/json'})
    torrentData = json.loads(raw_data.content)
    if 'error' not in torrentData and 'torrent' in torrentData:
        if len(torrentData['torrent']) > 0 and 'value' in torrentData['torrent'][0]:
            return str(torrentData['torrent'][0]['value'])
        else:
            return ''
    else:
        return str(torrentData)
