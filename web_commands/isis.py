# coding=utf-8
import random

import feedparser


def run(keyConfig, message, totalResults=1):
    realUrl = 'http://isis.liveuamap.com/rss'
    data = feedparser.parse(realUrl)
    if len(data.entries) >= 1:
        return data.entries[random.randint(0, 9)].link
    else:
        return 'I\'m sorry Dave, I\'m afraid I can\'t find any ISIS news.'