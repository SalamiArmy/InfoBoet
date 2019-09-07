import main
pronounce = main.get_platform_command_code('telegram', 'pronounce')
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    pronounce.run(bot, chat_id, user, keyConfig, message, totalResults)
