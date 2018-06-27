import ConfigParser
import unittest
import telegram
from commands import add

from google.appengine.ext import ndb
from google.appengine.ext import testbed

class TestGetMP3(unittest.TestCase):
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

    def test_getmp3(self):
        add.setTelegram_CommandCode('getvid', open('../telegram_commands/getvid.py').read())
        import telegram_commands.getmp3 as getmp3
        requestText = 'trippy swirl'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        getmp3.run(bot, chatId, 'Admin', keyConfig, requestText)

    def test_getmp3_group(self):
        add.setTelegram_CommandCode('getvid', open('../telegram_commands/getvid.py').read())
        import telegram_commands.getmp3 as getmp3
        requestText = 'hippie sabotage - high enough'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_GROUP_CHAT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID')

        getmp3.run(bot, chatId, 'Admin', keyConfig, requestText)
