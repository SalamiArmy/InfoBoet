import ConfigParser
import unittest
import telegram

import commands.wiki as wiki


class TestWiki(unittest.TestCase):
    def test_wiki(self):
        requestText = 'chloe bennet'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        bot.sendMessage(chat_id=chatId, text=wiki.run('SalamiArmy', requestText, chatId, 5))
