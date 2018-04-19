import ConfigParser
import unittest

import telegram

import commands.bitcoin as bitcoin
from google.appengine.ext import testbed


class TestBitcoin(unittest.TestCase):
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

    def test_bitcoin(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        bitcoin.run(bot, chatId, 'Admin', keyConfig, 'ETH')

    def test_bitcoin_group(self):
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID')

        bitcoin.run(bot, chatId, 'Admin', keyConfig)
