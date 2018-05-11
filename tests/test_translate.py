# coding=utf-8
import ConfigParser
import unittest
import telegram

import telegram_commands.translate as translate


class TestTorrent(unittest.TestCase):
    def test_translate_in_group_chat(self):
        requestText = 'Gesù Christi'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        bot.sendMessage(chat_id=chatId, text=translate.run('Admin', requestText, chatId))

    def test_translate_in_private_chat(self):
        requestText = 'Deutsche Vermögensberatung'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        bot.sendMessage(chat_id=chatId, text=translate.run('Admin', requestText, chatId))
