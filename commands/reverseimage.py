# coding=utf-8
import json
from google.appengine.api import urlfetch


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    bot.sendMessage(chat_id=chat_id, text=user +', I see ' + vision_web_entities(requestText, keyConfig))

def vision_web_entities(image_link, key_config):
    strPayload = str({
            "requests":
                [
                    {
                        "features":
                            [
                                {
                                    "type": "WEB_DETECTION"
                                }
                            ],
                        "image":
                            {
                                "source":
                                    {
                                        "imageUri": str(image_link)
                                    }
                            }
                    }
                ]
        })
    raw_data = urlfetch.fetch(
        url='https://vision.googleapis.com/v1/images:annotate?key=' + key_config.get('Google', 'GCSE_APP_ID'),
        payload=strPayload,
        method='POST',
        headers={'Content-type': 'application/json'})
    data = json.loads(raw_data.content)
    if 'error' not in data:
        if 'error' not in data['responses'][0]:
            strWebEntities = ''
            for entity in data['responses'][0]['webDetection']['webEntities']:
                strWebEntities += entity['description'] + ', '
            strFullMatchingImages = ''
            for image in data['responses'][0]['webDetection']['fullMatchingImages']:
                strFullMatchingImages += image['url'] + ', '
            strPartialMatchingImages = ''
            for image in data['responses'][0]['webDetection']['partialMatchingImages']:
                strPartialMatchingImages += image['url'] + ', '
            strPagesWithMatchingImages = ''
            for image in data['responses'][0]['webDetection']['pagesWithMatchingImages']:
                strPagesWithMatchingImages += image['url'] + ', '
            strVisuallySimilarImages = ''
            for image in data['responses'][0]['webDetection']['visuallySimilarImages']:
                strVisuallySimilarImages += image['url'] + ', '
            return strWebEntities.rstrip(', ') + '\n' + \
                   'Full Matching Images: ' + strFullMatchingImages.rstrip(', ') + '\n' + \
                   'Partial Matching Images: ' + strPartialMatchingImages.rstrip(', ') + '\n' + \
                   'Pages With Matching Images: ' + strPagesWithMatchingImages.rstrip(', ') + '\n' + \
                   'Visually Similar Images: ' + strVisuallySimilarImages.rstrip(', ')
        else:
            return data['responses'][0]['error']['message']
    else:
        return data['error']['message']