import ConfigParser
import unittest
import telegram

import commands.getquote as getquote


class TestGetQuote(unittest.TestCase):
    def test_getquote(self):
        requestText = 'critters of hollywood'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        bot.sendMessage(chat_id=chatId, text=getquote.run('Admin', requestText, chatId))

    def test_getquote_group(self):
        requestText = 'cook pu'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_GROUP_CHAT_ID')

        bot.sendMessage(chat_id=chatId, text=getquote.run('SalamiArmy', requestText, chatId))
