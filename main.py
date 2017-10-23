# coding=utf-8
import ConfigParser
import importlib
import json
import logging
import urllib
import sys

import urllib2

import imp
import telegram

# standard app engine imports
from google.appengine.api import urlfetch

import webapp2

from commands import add

BASE_URL = 'https://api.telegram.org/bot'

# Read keys.ini file at program start (don't forget to put your keys in there!)
keyConfig = ConfigParser.ConfigParser()
keyConfig.read(["keys.ini", "..\keys.ini"])
keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])

bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))

# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(
            BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(
            BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(
                BASE_URL + keyConfig.get('Telegram', 'TELE_BOT_ID') + '/setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(120)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        if 'message' in body or 'edited_message' in body:
            message = body['message'] if 'message' in body else body['edited_message']
            text = ''
            if 'text' in message:
                text = message['text'].encode('utf-8')
            fr = message.get('from')
            user = fr['username'].encode('utf-8') \
                if 'username' in fr \
                else fr['first_name'].encode('utf-8') + ' ' + fr['last_name'].encode('utf-8') \
                if 'first_name' in fr and 'last_name' in fr \
                else fr['first_name'].encode('utf-8') if 'first_name' in fr \
                else 'Dave'
            if 'edited_message' in body:
                user += '(editted)'
            chat = message['chat']
            chat_id = chat['id']
            chat_type = chat['type']

            if not text:
                logging.info('no text')
                return

            if text.startswith('/'):
                self.TryExecuteExplicitCommand(chat_id, user, text, chat_type)

    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        command = self.request.get('command')
        message = self.request.get('message')
        if command == 'define':
            from commands import define
            data = define.get_define_data(keyConfig, 'Admin', message)
            return data
        else:
            return 'unknown command'

    def TryExecuteExplicitCommand(self, chat_id, fr_username, text, chat_type):
        split = text[1:].split(' ', 1)
        try:
            commandName = split[0].lower().replace(bot.name.lower(), '')
            totalResults = 1
            import re
            if len(re.findall('^[a-z]+\d+$', commandName)) > 0:
                totalResults = re.findall('\d+$', commandName)[0]
                commandName = re.findall('^[a-z]+', commandName)[0]
            if commandName != 'say' and commandName != 'add':
                mod = importlib.import_module('commands.' + commandName)
                mod.run(bot, chat_id, fr_username, keyConfig, split[1] if len(split) > 1 else '', totalResults)
        except ImportError:
            if chat_type == 'private':
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (fr_username if not fr_username == '' else 'Dave') +
                                                      ', I\'m afraid I do not recognize the ' + commandName + ' command.')
        except:
            print("Unexpected Exception running command:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))
            try:
                bot.sendMessage(chat_id=keyConfig.get('BotAdministration', 'TESTING_GROUP_CHAT_ID'),
                                text='I\'m sorry Admins, I\'m afraid there\'s been an error. For ' + fr_username +
                                     '\'s request ' + (('\'' + split[1] + '\'') if len(split) > 1 else '') +
                                     '. Command ' + split[0] + ' threw:\n' +
                                     str(sys.exc_info()[0]) + '\n' + str(sys.exc_info()[1]))
            except:
                print("Unexpected error sending error response:",  str(sys.exc_info()[0]) + str(sys.exc_info()[1]))

def load_code_as_module(module_name):
    get_value_from_data_store = add.CommandsValue.get_by_id(module_name)
    if get_value_from_data_store:
        command_code = str(get_value_from_data_store.codeValue)
        if command_code != '':
            module = imp.new_module(module_name)
            try:
                exec command_code in module.__dict__
            except ImportError:
                print module_name + '\n' + \
                      'imports between commands must be replaced with command = main.load_code_as_module(command) ' + \
                      'for Scenic Oxygen to be able to resolve them' + \
                      str(sys.exc_info()[0]) + '\n' + \
                      str(sys.exc_info()[1]) + '\n' + \
                      command_code
                return None
            return module
    return None


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler)
], debug=True)
