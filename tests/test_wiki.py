import ConfigParser
import unittest
import telegram

import telegram_commands.wiki as wiki


class TestWiki(unittest.TestCase):
    def test_muli_wiki(self):
        requestText = 'chloe bennet'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        bot.sendMessage(chat_id=chatId, text=wiki.run('SalamiArmy', requestText, chatId, 5))

    def test_wiki_group(self):
        requestText = 'Invention Secrecy act'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TESTING_TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID')

        bot.sendMessage(chat_id=chatId, text=wiki.run(bot, chatId, 'shaun420', keyConfig, requestText, 1))
