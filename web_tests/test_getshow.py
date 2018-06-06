import ConfigParser
import unittest

import telegram
from google.appengine.ext import ndb
from google.appengine.ext import testbed

import main
from commands import add


class TestGetShow(unittest.TestCase):
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

    def test_getshow(self):
        requestText = u'pussy'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        add.setCommandCode('getshow', open('../commands/getshow.py').read())
        getshow = main.load_code_as_module('getshow')
        getshow.run('Admin', requestText, chatId)

    def test_getshow_group(self):
        requestText = u'Mike & Molly'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID')

        add.setCommandCode('getshow', open('../commands/getshow.py').read())
        getshow = main.load_code_as_module('getshow')
        getshow.run(bot, chatId, 'SalamiArmy', keyConfig, requestText)
