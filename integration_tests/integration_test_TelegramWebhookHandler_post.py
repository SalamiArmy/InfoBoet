# coding=utf-8
import ConfigParser
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import main
from commands import add


class TestTelegramWebhookHandlerPost(unittest.TestCase):
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

    def integration_test_translate_post(self):
        add.setTelegram_CommandCode('getshow', open('../commands/getshow.py').read())
        newRequestObject = main.TelegramWebhookHandler()
        class Object(object):
            pass
        newRequestObject.request = Object()
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        newRequestObject.request.body = '{"message": {"from": {"username": "SalamiArmy", "first_name": "Ashley", "last_name": "Lewis"}, "text": "/getshow godless", "chat": {"id": ' + keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID') + ', "type": "group"}}}'
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: None
        newRequestObject.post()

    def integration_test_reverseimage_post(self):
        add.setTelegram_CommandCode('reverseimage', open('../commands/reverseimage.py').read())
        newRequestObject = main.TelegramWebhookHandler()
        class Object(object):
            pass
        newRequestObject.request = Object()
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        newRequestObject.request.body = '{"message": {"from": {"username": "SalamiArmy", "first_name": "Ashley", "last_name": "Lewis"}, "text": "/reverseimage http://i.imgur.com/dRrbitg.gif", "chat": {"id": ' + keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID') + ', "type": "group"}}}'
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: None
        newRequestObject.post()

    def integration_test_getlink_post(self):
        add.setTelegram_CommandCode('getlink', open('../commands/getlink.py').read())
        newRequestObject = main.TelegramWebhookHandler()
        class Object(object):
            pass
        newRequestObject.request = Object()
        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        newRequestObject.request.body = '{"message": {"from": {"username": "SalamiArmy", "first_name": "Ashley", "last_name": "Lewis"}, "text": "/getlink10 world of warcraft classic", "chat": {"id": ' + keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID') + ', "type": "group"}}}'
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: None
        newRequestObject.post()
