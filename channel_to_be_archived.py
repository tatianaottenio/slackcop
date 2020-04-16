import os
import logging
from slack import WebClient
import time
import ssl as ssl_lib
import certifi
from channels_list import ChannelsList

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_USER_TOKEN'],ssl=True)

def channels_to_be_archived(channels):
    three_months_ago = time.time() - 2*30*24*60*60;

    for c in channels:
        response_hst = slack_web_client.conversations_history(
            channel=c["id"],
            oldest=str(three_months_ago)
        )

        messages = response_hst["messages"]
        valid_subtypes = ["bot_message", "message_replied", "thread_broadcast"]

        archive=True
        for m in messages:
            if "subtype" not in m or m["subtype"] in valid_subtypes:
                archive=False
                break

        print(c["id"], ",", c["name"], ",", archive)



if __name__ == "__main__":
    #logger = logging.getLogger()
    #logger.setLevel(logging.DEBUG)
    #logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

    channels = ChannelsList.listChannels()
    print(len(channels), '\n\n\n\n')
    channels_to_be_archived(channels)
