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

REGEX_PREFIX="^team-|^proj-|^bot-|^livup-|^local-|^temp-|^-help|^learn-|^off-|^outros-"
MESSAGE="Hey, channel! Preciso da ajuda de vocês para mantermos o Slack organizado.\nEsse canal está com o nome fora dos nossos padrões.\nÉ facinho arrumar! Não leva nem 2 minutos. Se você criou o canal, vá em `Detalhes > Mais > Renomear canal` e coloca um dos prefixos dessa lista: https://bit.ly/2XJgbY2\n\nSe estiver com dificuldades, é só chamar no #temp-slack-channels. Obrigado!"
LOGGER = logging.getLogger()


# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'],ssl=True)

#@app.route('/slack/channels/clean')
def verify_channels_name(channels):
    LOGGER.info("Channels:")
    for c in channels:
        channel_name = c["name"]
        hasPrefix = re.search(REGEX_PREFIX, channel_name)

        if (hasPrefix):
            continue

        try:
            LOGGER.info("%s", channel_name)
            response_message = slack_web_client.chat_postMessage(
                channel=c["id"],
                text=MESSAGE
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            LOGGER.error("Got an error for channel %s: %s", channel_name, e.response['error'])

if __name__ == "__main__":
    LOGGER.addHandler(logging.StreamHandler())
    LOGGER.setLevel(logging.INFO)

    #logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

    #Get all active channels
    channels_list = ChannelsList()
    channels = channels_list.list_channels()

    #channels=[{"id":"1", "name": "blabkabak"}]

    LOGGER.info("Verifying %d channels", len(channels))
    #LOGGER.info("Channels: %s", str(channels))

    verify_channels_name(channels)
