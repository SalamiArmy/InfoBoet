from commands import add


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    try:
        es = add.CommandsValue.query().fetch()
        available_commands = []
        if len(es) > 0:
            for mod in es:
                available_commands.append(str(mod.key._Key__pairs[0][1]))
        bot.sendMessage(chat_id=chat_id, text="I know:\n" + "\n".join(available_commands))
        return True
    except:
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                              ', I\'m afraid there\'s no helping you.')
