# coding=utf-8
import json
from google.appengine.api import urlfetch


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    bot.sendMessage(chat_id=chat_id, text=user +', I see ' + vision_web_entities(requestText, keyConfig))

def vision_web_entities(image_link, key_config):
    global strFullMatchingImages, strPartialMatchingImages, strPagesWithMatchingImages, strVisuallySimilarImages
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
            if ('fullMatchingImages' in webDetection):
                strFullMatchingImages = 'Full Matching Images: '
                for image in webDetection['fullMatchingImages']:
                    strFullMatchingImages += image['url'] + ', '
                strVisuallySimilarImages = strVisuallySimilarImages.rstrip(', ') + '\n'
            if ('partialMatchingImages' in webDetection):
                strPartialMatchingImages = 'Partial Matching Images: '
                for image in webDetection['partialMatchingImages']:
                    strPartialMatchingImages += image['url'] + ', '
                strVisuallySimilarImages = strVisuallySimilarImages.rstrip(', ') + '\n'
            if ('pagesWithMatchingImages' in webDetection):
                strPagesWithMatchingImages = 'Pages With Matching Images: '
                for image in webDetection['pagesWithMatchingImages']:
                    strPagesWithMatchingImages += image['url'] + ', '
                strVisuallySimilarImages = strVisuallySimilarImages.rstrip(', ') + '\n'
            if ('visuallySimilarImages' in webDetection):
                strVisuallySimilarImages = 'Visually Similar Images: '
                for image in webDetection['visuallySimilarImages']:
                    strVisuallySimilarImages += image['url'] + ', '
                strVisuallySimilarImages = strVisuallySimilarImages.rstrip(', ')
            return strWebEntities.rstrip(', ') + '\n' + \
                   strFullMatchingImages + \
                   strPartialMatchingImages + \
                   strPagesWithMatchingImages + \
                   strVisuallySimilarImages
        else:
            return data['responses'][0]['error']['message']
    else:
        return data['error']['message']