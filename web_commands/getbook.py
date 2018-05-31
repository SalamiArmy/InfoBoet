# coding=utf-8
import ConfigParser
import urllib
from bs4 import BeautifulSoup

from google.appengine.ext import ndb

class SeenBooks(ndb.Model):
    seenBook = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setPreviouslySeenBooksValue(NewValue):
    es = SeenBooks.get_or_insert()
    es.seenBook = NewValue
    es.put()

def getPreviouslySeenBooksValue(bookValue):
    es = SeenBooks.get_or_insert()
    if es.seenBook:
        return True
    setPreviouslySeenBooksValue(bookValue)
    return False


def run(keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    args = {'key': keyConfig.get('GoodReads', 'KEY'),
            'search[field]': 'all',
            'safe': 'off',
            'q': requestText,
            'page': 1}
    realUrl = 'https://www.goodreads.com/search/index.xml?' + urllib.urlencode(args)
    raw_xml_data = urllib.urlopen(realUrl).read()
    bookTitles, ratings, total_ratings, bookIDs, bookDescriptions = book_results_parser(raw_xml_data, keyConfig)

    offset = 0
    result = ''
    while int(offset) < int(totalResults) and offset < len(bookTitles):
        bookTitle = bookTitles[offset]
        if not getPreviouslySeenBooksValue(bookTitle):
            bookData = FormatDesc(bookDescriptions[offset])
            url = 'https://www.goodreads.com/book/show/' + bookIDs[offset] + '-' + requestText.replace(' ', '-')
            rating = ratings[offset]
            total_rating = total_ratings[offset]
            formatted_book_data = bookTitle + (' ' + str(offset+1) + ' of ' + str(totalResults) if int(totalResults) > 1 else '') + '*\n' +\
                                  ('_Rated ' + rating.encode('utf-8') + ' out of 5 by ' +
                                   total_rating + ' GoodReads users._\n' if rating.encode('utf-8') == '0' else '')\
                                  + bookData.replace('***', '') + '\n' + url
            result = formatted_book_data
        offset += 1
    if len(bookTitles) <= 0 or offset < totalResults:
        result = 'I\'m sorry Dave' + ', I\'m afraid I can\'t find any books' + (
        ' that you haven\'t already seen' if len(bookTitles) > 0 and offset > 0 else '') + ' for ' + str(requestText) \
                 + '.'
    return result

def FormatDesc(Desc):
    return Desc.replace('<br />', '\n')\
        .replace('<i>', '_')\
        .replace('</i>', '_')\
        .replace('<em>', '*')\
        .replace('</em>', '*')\
        .replace('<p>', '\n')\
        .replace('</p>', '\n')\
        .replace('<b>', '*')\
        .replace('</b>', '*')



def book_results_parser(rawMarkup, keyConfig):
    soup = BeautifulSoup(rawMarkup)
    bookDescriptions = []
    bookIDs = []
    bookTitles = []
    bookAverageRatings = []
    bookRatingsCounts = []
    for book in soup.findAll('best_book'):
        bookId = book.findAll('id')[0].string
        realUrl = 'https://www.goodreads.com/book/show.xml?key=' + keyConfig.get('GoodReads', 'KEY') + '&id=' + bookId
        raw_xml_object = urllib.urlopen(realUrl).read()
        data = BeautifulSoup(raw_xml_object)
        bookIDs.append(data.findAll('id')[0].string)
        bookDescriptions.append(data.findAll('description')[0].string if data.findAll('description')[0].string != None else '')
        bookTitles.append(data.findAll('title')[0].string)
        bookAverageRatings.append(data.findAll('average_rating')[0].string)
        bookRatingsCounts.append(data.findAll('ratings_count')[0].string)
    return bookTitles, bookAverageRatings, bookRatingsCounts, bookIDs, bookDescriptions