# coding=utf-8
import ConfigParser
import unittest
import telegram

import commands.getlyrics as getlyrics


class TestGetLyrics(unittest.TestCase):
    def test_getlyrics(self):
        requestText = 'work that body'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TESTING_TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID')

        bot.sendMessage(chat_id=chatId, text=getlyrics.run('Admin', requestText, chatId))
