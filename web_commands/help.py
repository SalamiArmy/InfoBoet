from commands import add


def run(keyConfig, message, totalResults=1):
    try:
        es = add.CommandsValue.query().fetch()
        available_commands = []
        if len(es) > 0:
            for mod in es:
                available_commands.append(str(mod.key._Key__pairs[0][1]))
        return "I know:\n" + "\n".join(available_commands)
    except:
        return 'I\'m sorry Dave, I\'m afraid there\'s no helping you.'
