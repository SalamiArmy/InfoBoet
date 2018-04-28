# coding=utf-8
import json
import urllib

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    tvSearchText = GetTVSearchText(requestText)
    movieSearchText = GetMovieSearchText(requestText)

    if tvSearchText:
        bot.sendMessage(chat_id=chat_id, text='Serial Magent Link:\n' + tvSearchText + 'Movie Magent Link:\n' + movieSearchText)
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                              ', I can\'t find any torrents for ' + \
                                              requestText.encode('utf-8') + '.')

def GetTVSearchText(text):
    raw_data = urlfetch.fetch(
        url='https://oneom.tk/search/serial?limit=1&title=' + text,
        headers={'Accept': 'application/json'})
    torrentData = json.loads(raw_data.content)
    if 'error' not in torrentData and 'serials' in torrentData:
        if len(torrentData['serials']) > 0 and 'id' in torrentData['serials'][0]:
            return GetTVMagnetLink(str(torrentData['serials'][0]['id']))
        else:
            return ''
    else:
        return str(torrentData)

def GetTVMagnetLink(text):
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

def GetMovieSearchText(text):
    raw_data = urlfetch.fetch(url='https://yts.am/api/v2/list_movies.json?limit=1&' + urllib.urlencode({'query_term' : text}))
    torrentData = json.loads(raw_data.content)
    if 'error' not in torrentData and 'data' in torrentData and 'movies' in torrentData['data']:
        if len(torrentData['data']['movies']) > 0 and 'torrents' in torrentData['data']['movies'][0] and 'hash' in torrentData['data']['movies'][0]['torrents']:
            return GetMovieMagnetLink(str(torrentData['data']['movies'][0]['torrents']['hash']), torrentData['data']['movies'][0]['slug'])
        else:
            return ''
    else:
        return str(torrentData)

def GetMovieMagnetLink(torrentHash, slug):
    return 'magnet:?xt=urn:btih:' + torrentHash + '&dn=' + slug + '&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://glotorrents.pw:6969/announce&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://torrent.gresille.org:80/announce&tr=udp://p4p.arenabg.com:1337&tr=udp://tracker.leechers-paradise.org:6969' 
