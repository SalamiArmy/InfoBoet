import main
getirish = main.get_platform_command_code('telegram', 'getirish')
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    getirish.run(bot, chat_id, user, keyConfig, message, totalResults)
