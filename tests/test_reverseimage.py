import ConfigParser
import unittest
import telegram

import commands.reverseimage as reverseimage
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
        requestText = 'https://s-media-cache-ak0.pinimg.com/originals/e3/68/e2/e368e259e24b47d3b61eeed92a2e1b0d.gif'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))

        #for admin group
        chatId = keyConfig.get('BotAdministration', 'TESTING_GROUP_CHAT_ID')

        reverseimage.run(bot, chatId, 'Admin', keyConfig, requestText)
