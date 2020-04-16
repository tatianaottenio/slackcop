import os
import sys
import re
import logging
from slack import WebClient
from slack.errors import SlackApiError
import time
import ssl as ssl_lib
import certifi
from channels_list import ChannelsList


# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'],ssl=True)

REGEX_PREFIX="^team-|^proj-|^bot-|^livup-|^local-|^cd-|^temp-|^learn-|^off-|^outros-"
MESSAGE="Hey, channel! Preciso da ajuda de vocês para mantermos o Slack organizado.\nEsse canal está com o nome fora dos nossos padrões.\nÉ facinho arrumar! Não leva nem 2 minutos. Vá em `Detalhes > Mais > Renomear canal` e coloca um dos prefixos dessa lista: https://bit.ly/2XJgbY2\nObrigado!"

#@app.route('/slack/channels/clean')
def verify_channels_name(channels):
    for c in channels:
        channelName = c["name"]
        hasPrefix = re.search(REGEX_PREFIX, channelName)

        if (hasPrefix):
            continue

        try:
            print(channelName)
            response_message = slack_web_client.chat_postMessage(
                channel=c["id"],
                text=MESSAGE
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")

if __name__ == "__main__":
    #logger = logging.getLogger()
    #logger.setLevel(logging.DEBUG)
    #logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

    channels_list = ChannelsList()
    channels = channels_list.list_channels()

    print(len(channels))

    verify_channels_name([])
