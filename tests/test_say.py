# coding=utf-8
import ConfigParser
import unittest
import telegram

import commands.say as say
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class TestSay(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_urlfetch_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def test_say(self):
        requestText = u'It\'s said that women and men are from two different planets when it comes to communication'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini", "keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = int(keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID'))

        say.run(bot, chatId, 'SalamiArmy', keyConfig, requestText, 1)

    def test_say_group(self):
        requestText = u'cuunt vag mate'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TESTING_TELEGRAM_BOT_ID'))
        chatId = int(keyConfig.get('BotAdministration', 'TESTING_GROUP_CHAT_ID'))

        say.run(bot, chatId, 'SalamiArmy', keyConfig, requestText, 1)
