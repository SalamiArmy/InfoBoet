# coding=utf-8
import json
import urllib
import urllib2

def run(keyConfig, message, totalResults=1):
    requestText = message.strip()
    url = 'https://api.cognitive.microsoft.com/bing/v5.0/suggestions/'
    values = {'q': requestText}

    data = urllib.urlencode(values)
    req = urllib2.Request(url + '?' + data)
    req.add_header('Ocp-Apim-Subscription-Key', keyConfig.get('Bing', 'AutoSuggestApiKey'))
    try:
        data = json.load(urllib2.urlopen(req))
    except urllib2.HTTPError:
        print('HTTP Error: ' + url + '?' + data)

    if 'suggestionGroups' in data and len(data['suggestionGroups']) >= 1 and 'searchSuggestions' in data['suggestionGroups'][0] and len(data['suggestionGroups'][0]['searchSuggestions']) >= 1 and 'displayText' in data['suggestionGroups'][0]['searchSuggestions'][0] and data['suggestionGroups'][0]['searchSuggestions'][0]['displayText'] != requestText:
        returnText = ''
        for searchSuggestion in data['suggestionGroups'][0]['searchSuggestions']:
            returnText += searchSuggestion['displayText'] + '\n'
        return requestText + '...\n' + returnText
    else:
        return 'I\'m sorry Dave, I\'m afraid I can\'t find a suggestion for ' + requestText + '.'
