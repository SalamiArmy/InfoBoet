# coding=utf-8
import soundcloud
from google.appengine.ext import ndb


class SeenTracks(ndb.Model):
    # key name: get:str(chat_id)
    allPreviousHeardTracks = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenTracksValue(chat_id, NewValue):
    es = SeenTracks.get_or_insert(str(chat_id))
    es.allPreviousHeardTracks = NewValue.encode('utf-8')
    es.put()

def addPreviouslySeenTracksValue(chat_id, NewValue):
    es = SeenTracks.get_or_insert(str(chat_id))
    if es.allPreviousHeardTracks == '':
        es.allPreviousHeardTracks = NewValue.encode('utf-8').replace(',', '')
    else:
        es.allPreviousHeardTracks += ',' + NewValue.encode('utf-8').replace(',', '')
    es.put()

def getPreviouslySeenTracksValue(chat_id):
    es = SeenTracks.get_or_insert(str(chat_id))
    if es:
        return es.allPreviousHeardTracks.encode('utf-8')
    return ''

def wasPreviouslySeenTrack(chat_id, url):
    url = url.replace(',', '')
    allPreviousTracks = getPreviouslySeenTracksValue(chat_id)
    if ',' + url + ',' in allPreviousTracks or \
            allPreviousTracks.startswith(url + ',') or \
            allPreviousTracks.endswith(',' + url) or \
            allPreviousTracks == url:
        return True
    return False


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()

    tracks = get_tracks(keyConfig, requestText)
    if len(tracks) >= 1:
        for track in tracks:
            track_url = track.permalink_url
            if not wasPreviouslySeenTrack(chat_id, track_url):
                addPreviouslySeenTracksValue(chat_id, track_url)
                bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + track_url)
                return True
    else:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid I can\'t find the sound of ' +
                                              requestText.encode('utf-8') + '.')


def get_tracks(keyConfig, requestText):
    client = soundcloud.Client(client_id=keyConfig.get('Soundcloud', 'SC_CLIENT_ID'))
    tracks = client.get('/tracks', q=requestText.encode('utf-8'), sharing='public')
    return tracks
