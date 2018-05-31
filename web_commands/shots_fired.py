def run(keyConfig, message, totalResults=1):
    try:
        target = message.split(" ")[message.split(" ").index("shots_fired") + 1]
        return "pew PEW pew " + target + " PEW pew PEW")
    except:
        return "pew pew PEW PEW PEW")
    return True
