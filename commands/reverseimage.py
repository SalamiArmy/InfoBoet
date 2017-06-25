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
        if 'error' not in data['responses'][0] and 'webDetection' in data['responses'][0]:
            webDetection = data['responses'][0]['webDetection']
            strWebEntities = ''
            if ('webEntities' in webDetection):
                for entity in webDetection['webEntities']:
                    strWebEntities += entity['description'] + ', '
            strFullMatchingImages = ''
            if ('fullMatchingImages' in webDetection):
                for image in webDetection['fullMatchingImages']:
                    strFullMatchingImages += image['url'] + ', '
            strPartialMatchingImages = ''
            if ('partialMatchingImages' in webDetection):
                for image in webDetection['partialMatchingImages']:
                    strPartialMatchingImages += image['url'] + ', '
            strPagesWithMatchingImages = ''
            if ('pagesWithMatchingImages' in webDetection):
                for image in webDetection['pagesWithMatchingImages']:
                    strPagesWithMatchingImages += image['url'] + ', '
            strVisuallySimilarImages = ''
            if ('visuallySimilarImages' in webDetection):
                for image in webDetection['visuallySimilarImages']:
                    strVisuallySimilarImages += image['url'] + ', '
            return strWebEntities.rstrip(', ') + '\n' + \
                   ('Full Matching Images: ' + strFullMatchingImages.rstrip(', ') + '\n' if strFullMatchingImages != '' else '') + \
                   ('Partial Matching Images: ' + strPartialMatchingImages.rstrip(', ') + '\n' if strPartialMatchingImages != '' else '') + \
                    ('Pages With Matching Images: ' + strPagesWithMatchingImages.rstrip(', ') + '\n' if strPagesWithMatchingImages != '' else '') + \
                     ('Visually Similar Images: ' + strVisuallySimilarImages.rstrip(', ') if strVisuallySimilarImages != '' else '')
        else:
            return data['responses'][0]['error']['message']
    else:
        return data['error']['message']