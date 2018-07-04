
import main
place = main.get_platform_command_code('telegram', 'place')
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    place.run(bot, chat_id, user, keyConfig, message, totalResults)
