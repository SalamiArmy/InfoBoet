import ConfigParser
import unittest
import telegram

import telegram_commands.getweather as getweather


class TestGetWeather(unittest.TestCase):
    def test_getweather(self):
        requestText = 'ixopo'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        getweather.run(bot, chatId, 'Admin', keyConfig, requestText)
