import os
import sys
import logging
from slack import WebClient
from slack.errors import SlackApiError
import time
import ssl as ssl_lib
import certifi
from channels_list import ChannelsList

INACTIVE_DAYS=60
LOGGER = logging.getLogger()

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'],ssl=True)

#@app.route('/slack/channels/clean')
def archive_channels(channelsIds):
    for id in channelsIds:
        try:
            LOGGER.info("======== %d",id)
            response_join = slack_web_client.conversations_join(
                channel=id
            )

            LOGGER.info("join ok")
            response_arch = slack_web_client.conversations_archive(
                channel=id
            )

            LOGGER.info("archive ok")
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            LOGGER.error("Got an error: %s:", e.response['error'])


if __name__ == "__main__":
    LOGGER.addHandler(logging.StreamHandler())
    LOGGER.setLevel(logging.INFO)

    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

    channelsIds = []
    #Channels id coming from command line
    if len(sys.argv) > 1:
        LOGGER.info("Using IDs sent via command line")
        channelsIds = sys.argv[1:]
    else:
        LOGGER.info("Using IDs from Slack API")
        channels_list = ChannelsList()
        channelsIds = channels_list.list_channels_to_be_archived(INACTIVE_DAYS)

    LOGGER.info("Verifying %d channels", len(channelsIds))
    LOGGER.info("Ids: %s", str(channelsIds))

    archive_channels(channelsIds)
