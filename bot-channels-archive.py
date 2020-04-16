import os
import logging
from slack import WebClient
from slack.errors import SlackApiError
import time
import ssl as ssl_lib
import certifi
from channels_list import ChannelsList


# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'],ssl=True)

#@app.route('/slack/channels/clean')
def archive_channels(channels):
    for id in channels:
        try:
            print("========",id)
            response_join = slack_web_client.conversations_join(
                channel=id
            )

            print("join ok"])
            response_arch = slack_web_client.conversations_archive(
                channel=id
            )

            print("archive ok"])
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
        finally:
            print("========")

if __name__ == "__main__":
    #logger = logging.getLogger()
    #logger.setLevel(logging.DEBUG)
    #logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    channels = ChannelsList.list_channels_to_be_archived(60)
    print(len(channels))
    channels_archive(channels)
