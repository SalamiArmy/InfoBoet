import ConfigParser
import unittest
import telegram

import telegram_commands.reverseimage as reverseimage
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class TestReverseImage(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        self.testbed.init_urlfetch_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def test_reverseimage(self):
        requestText = 'http://i.imgur.com/dRrbitg.gif'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        reverseimage.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_reverseimage_group(self):
        requestText = 'https://s-media-cache-ak0.pinimg.com/originals/fd/40/85/fd408599ae5d5b533445ff8c9b46b735.gif'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

        #for admin group
        chatId = keyConfig.get('BotAdministration', 'TESTING_GROUP_CHAT_ID')

        reverseimage.run(bot, chatId, 'SalamiArmy', keyConfig, requestText)
