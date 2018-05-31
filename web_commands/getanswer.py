# coding=utf-8
import tungsten

def run(keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    client = tungsten.Tungsten(keyConfig.get('Wolfram', 'WOLF_APP_ID'))
    result = client.query(requestText)
    allAnswers = result.pods
    if len(allAnswers) > 0:
        fullAnswer = ''
        for question in allAnswers[0].format['plaintext']:
            if question is not None:
                fullAnswer += question + '?\n'
        if len(allAnswers) > 1:
            for pod in allAnswers[1:]:
                for answer in pod.format['plaintext']:
                    if answer is not None:
                        fullAnswer += answer + '.\n'
        result = 'Dave' + fullAnswer
    else:
        result = 'I\'m sorry Dave, I\'m afraid I can\'t find any answers for ' + str(requestText)
    return result
