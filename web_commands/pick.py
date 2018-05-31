import random


def choose(msg):
    split = msg.split(" ")
    return split[random.randrange(0, len(split))]

def run(keyConfig, message, totalResults=1):
    return choose(message)
