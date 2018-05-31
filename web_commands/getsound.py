# coding=utf-8
import soundcloud
from google.appengine.ext import ndb


class SeenTracks(ndb.Model):
    # key name: get:str(chat_id)
    heardTrack = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setPreviouslySeenTracksValue(NewValue):
    es = SeenTracks.get_or_insert()
    es.heardTrack = NewValue
    es.put()

def addPreviouslySeenTracksValue(NewValue):
    es = SeenTracks.get_or_insert()
    if es.heardTrack == '':
        es.heardTrack = NewValue
    else:
        es.heardTrack += ',' + NewValue
    es.put()

def getPreviouslySeenTracksValue():
    es = SeenTracks.get_or_insert()
    if es:
        return es.heardTrack
    return False

def wasPreviouslySeenTrack(url):
    url = url.replace(',', '')
    allPreviousTracks = getPreviouslySeenTracksValue()
    if ',' + url + ',' in allPreviousTracks or \
            allPreviousTracks.startswith(url + ',') or \
            allPreviousTracks.endswith(',' + url) or \
            allPreviousTracks == url:
        return True
    return False


def run(keyConfig, message, totalResults=1):
    requestText = message.strip()

    tracks = get_tracks(keyConfig, requestText)
    if len(tracks) >= 1:
        for track in tracks:
            track_url = track.permalink_url
            if not wasPreviouslySeenTrack(track_url):
                addPreviouslySeenTracksValue(track_url)
                return track_url
    else:
        return 'I\'m sorry Dave, I\'m afraid I can\'t find the sound of ' + str(requestText) + '.'


def get_tracks(keyConfig, requestText):
    client = soundcloud.Client(client_id=keyConfig.get('Soundcloud', 'SC_CLIENT_ID'))
    tracks = client.get('/tracks', q=requestText.encode('utf-8'), sharing='public')
    return tracks
