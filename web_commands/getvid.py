# coding=utf-8
import json
import urllib
import string
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

class WhosSeenVideoUrls(ndb.Model):
    # key name: VideoUrl
    seenVideo = ndb.BooleanProperty(indexed=False, default=False)
    
def addPreviouslySeenVideosValue(video_url):
    es = WhosSeenVideoUrls.get_or_insert(video_url)
    es.seenVideo = True
    es.put()
    
def getseenVideosValue(video_link):
    es = WhosSeenVideoUrls.get_or_insert(video_link)
    return es.seenVideo

def wasPreviouslySeenVideo(video_link):
    allWhoveSeenVideo = getseenVideosValue(video_link)
    if allWhoveSeenVideo.seenVideo:
        return True
    addPreviouslySeenVideosValue(video_link)
    return False

def run(keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    args = {'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'type': 'video',
            'safeSearch': 'none',
            'q': requestText,
            'part': 'snippet',
            'maxResults': 25}
    return Send_Videos(requestText, args, keyConfig, totalResults)

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

def Send_Videos(requestText, args, keyConfig, total_number_to_send=1):
    data, total_results, results_this_page = Google_Custom_Search(args)
    if 'items' in data and total_results > 0:
        total_offset, total_results, total_sent = search_results_walker(args, data, total_number_to_send,
                                                                        requestText, results_this_page,
                                                                        total_results, keyConfig)
        if len(total_sent) < int(total_number_to_send):
            if int(total_number_to_send) > 1:
                return 'I\'m sorry Dave, I\'m afraid I can\'t find any more videos for ' +\
                                                      string.capwords(requestText.encode('utf-8') + '.' +
                                                                      ' I could only find ' + str(
                                                          len(total_sent)) + ' out of ' + str(total_number_to_send))
            else:
                return 'I\'m sorry Dave, I\'m afraid I can\'t find any videos for ' +\
                                                      string.capwords(str(requestText))
        return total_sent
    else:
        if 'error' in data:
            errorMsg = 'I\'m sorry Dave' +\
                       data['error']['message']
            return errorMsg
            return [errorMsg]
        else:
            errorMsg = 'I\'m sorry Dave' + \
                       ', I\'m afraid I can\'t find any videos for ' + \
                       string.capwords(requestText.encode('utf-8'))
            return errorMsg
            return [errorMsg]

def search_results_walker(args, data, number, requestText, results_this_page, total_results, keyConfig,
                          total_offset=0, total_sent=[]):
    offset_this_page = 0
    while len(total_sent) < int(number) and int(offset_this_page) < int(results_this_page):
        vidlink = str(data['items'][offset_this_page]['id']['videoId'])
        offset_this_page += 1
        total_offset = int(total_offset) + 1
        if is_valid_video(vidlink):
            if number == 1:
                return 'https://www.youtube.com/watch?v=' + vidlink + '&type=video'
                total_sent.append('https://www.youtube.com/watch?v=' + vidlink + '&type=video')
            else:
                message = requestText + ': ' + \
                          (str(len(total_sent) + 1) + ' of ' + str(number) + '\n' if int(number) > 1 else '') + \
                          'https://www.youtube.com/watch?v=' + vidlink + '&type=video'
                return message
                total_sent.append('https://www.youtube.com/watch?v=' + vidlink + '&type=video')
    if len(total_sent) < int(number) and int(total_offset) < int(total_results):
        args['pageToken'] = data['nextPageToken']
        data, total_results, results_this_page = Google_Custom_Search(args)
        return search_results_walker(args, bot, data, number, requestText, results_this_page, total_results, keyConfig,
                                     total_offset, total_sent)
    return total_offset, total_results, total_sent
