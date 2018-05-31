# coding=utf-8
import json
import urllib


def run(keyConfig, message, totalResults=1):
    return get_cric_data()

def get_cric_data():
    allMatchesUrl = 'http://cricscore-api.appspot.com/csa'
    getData = urllib.urlopen(allMatchesUrl).read().decode('utf-8')
    if ('<blockquote>' not in getData):
        allMatches = json.loads(getData)
        proteasMatchId = None
        for match in allMatches:
            if match['t1'] == 'South Africa' or match['t2'] == 'South Africa':
                proteasMatchId = match['id']
        if proteasMatchId == None:
            return 'I\'m sorry Dave, I\'m afraid the Proteas are not playing right now.'
        else:
            matchesUrl = 'http://cricscore-api.appspot.com/csa?id=' + str(proteasMatchId)
            match = json.load(urllib.urlopen(matchesUrl))
            return match[0]['si'] + '\n' + match[0]['de']
    else:
        return 'I\'m sorry Dave' + \
               getData[getData.index('<blockquote>') + len('<blockquote>'):getData.index('</blockquote>')]\
                   .replace('<H1>', '*')\
                   .replace('</H1>', '*')\
                   .replace('<p>', '')\
                   .replace('</p>', '')

