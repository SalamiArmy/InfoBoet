# coding=utf-8
import ConfigParser
import unittest

import telegram
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.api import urlfetch
from telegram_commands import define

import main

class TestDefine(unittest.TestCase):
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

    def integration_test_define(self):
        newRequestObject = main.WebhookHandler()
        class Object(object):
            pass
        newRequestObject.request = Object()
        newRequestObject.request.get = lambda x: 'define' if (x == 'command') else 'gosh'
        newRequestObject.response = Object()
        newRequestObject.response.write = lambda x: self.mockResponseWriter(x)
        self.responseString = ''
        newRequestObject.get()
        if self.responseString == '':
            raise Exception

    global responseString

    def mockResponseWriter(self, inputText):
        self.responseString = inputText
        return inputText