# coding=utf-8
import json
import urllib
from google.appengine.ext import ndb

CommandName = 'getvid'

class WhosSeenVideoUrls(ndb.Model):
    # key name: VideoUrl
    whoseSeenVideo = ndb.StringProperty(indexed=False, default='')
    
def addPreviouslySeenVideosValue(video_url, chat_id):
    es = WhosSeenVideoUrls.get_or_insert(video_url)
    if es.whoseSeenVideo == '':
        es.whoseSeenVideo = str(chat_id)
    else:
        es.whoseSeenVideo += ',' + str(chat_id)
    es.put()
    
def getwhoseSeenVideosValue(video_link):
    es = WhosSeenVideoUrls.get_or_insert(video_link)
    if es:
        return str(es.whoseSeenVideo)
    return ''

def wasPreviouslySeenVideo(video_link, chat_id):
    allWhoveSeenVideo = getwhoseSeenVideosValue(video_link)
    if ',' + str(chat_id) + ',' in allWhoveSeenVideo or \
            allWhoveSeenVideo.startswith(str(chat_id) + ',') or \
            allWhoveSeenVideo.endswith(',' + str(chat_id)) or \
                    allWhoveSeenVideo == str(chat_id):
        return True
    addPreviouslySeenVideosValue(videore_link, chat_id)
    return False

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).replace(bot.name, "").strip()
    args = {'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'type': 'video',
            'safeSearch': 'none',
            'q': requestText,
            'part': 'snippet'}
    return Send_Videos(bot, chat_id, user, requestText, args, keyConfig, totalResults)

def Google_Custom_Search(args):
    googurl = 'https://www.googleapis.com/youtube/v3/search'
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

def is_valid_video(video_url, chat_id):
    if video_url != '' and not wasPreviouslySeenVideo(video_url, chat_id):
        return True
    return False

def Send_Videos(bot, chat_id, user, requestText, args, keyConfig, total_number_to_send=1):
    data, total_results, results_this_page = Google_Custom_Search(args)
    if 'items' in data and total_results > 0:
        total_offset, total_results, total_sent = search_results_walker(args, bot, chat_id, data, total_number_to_send,
                                                                        user + ', ' + requestText, results_this_page,
                                                                        total_results, keyConfig)
        if len(total_sent) < int(total_number_to_send):
            if int(total_number_to_send) > 1:
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t find any more videos for ' +
                                                      string.capwords(requestText.encode('utf-8') + '.' +
                                                                      ' I could only find ' + str(
                                                          len(total_sent)) + ' out of ' + str(total_number_to_send)))
            else:
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t find any videos for ' +
                                                      string.capwords(requestText.encode('utf-8')))
        return total_sent
    else:
        if 'error' in data:
            errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                       data['error']['message']
            bot.sendMessage(chat_id=chat_id, text=errorMsg)
            return [errorMsg]
        else:
            errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                       ', I\'m afraid I can\'t find any videos for ' + \
                       string.capwords(requestText.encode('utf-8'))
            bot.sendMessage(chat_id=chat_id, text=errorMsg)
            return [errorMsg]

def search_results_walker(args, bot, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                          total_offset=0, total_sent=[]):
    offset_this_page = 0
    while len(total_sent) < int(number) and int(offset_this_page) < int(results_this_page):
        vidlink = str(data['items'][offset_this_page]['id']['videoId'])
        offset_this_page += 1
        total_offset = int(total_offset) + 1
        if is_valid_video(vidlink, chat_id):
            if number == 1:
                bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') +
                                'https://www.youtube.com/watch?v=' + vidlink + '&type=video')
                total_sent.append('https://www.youtube.com/watch?v=' + vidlink + '&type=video')
            else:
                message = requestText + ': ' + \
                          (str(len(total_sent) + 1) + ' of ' + str(number) + '\n' if int(number) > 1 else '') + 
                    'https://www.youtube.com/watch?v=' + vidlink + '&type=video'
                bot.sendMessage(chat_id=chat_id, text=message)
                total_sent.append('https://www.youtube.com/watch?v=' + vidlink + '&type=video')
    if len(total_sent) < int(number) and int(total_offset) < int(total_results):
        args['start'] = total_offset + 1
        data, total_results, results_this_page = Google_Custom_Search(args)
        return search_results_walker(args, bot, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                                     total_offset, total_sent)
    return total_offset, total_results, total_sent
