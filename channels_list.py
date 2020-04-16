import os
import logging
from slack import WebClient
import time
import ssl as ssl_lib
import certifi

class ChannelsList:
    #@app.route('/slack/channels/clean')
    @staticmethod
    def listChannels():
        # Initialize a Web API client
        slack_web_client = WebClient(token=os.environ['SLACK_USER_TOKEN'],ssl=True)

        response = slack_web_client.conversations_list(
            types="public_channel",
            exclude_archived="true",
            limit=200
        )
        channels = response["channels"]
        response_metadata = response["response_metadata"]

        while "next_cursor" in response_metadata and response_metadata["next_cursor"]:
            response = slack_web_client.conversations_list(
                types="public_channel",
                exclude_archived="true",
                limit=200,
                cursor=response_metadata["next_cursor"]
            )
            channels += response["channels"]

            response_metadata = response["response_metadata"]

        return channels

    @staticmethod
    def list_channels_to_be_archived(inactive_days):
        oldest = time.time() - inactive_days*24*60*60;

        idsToArchive = []
        for c in channels:
            response_hst = slack_web_client.conversations_history(
                channel=c["id"],
                oldest=str(oldest)
            )

            messages = response_hst["messages"]
            valid_subtypes = ["bot_message", "message_replied", "thread_broadcast"]

            archive=True
            for m in messages:
                if "subtype" not in m or m["subtype"] in valid_subtypes:
                    archive=False
                    break

            print(c["id"], ",", c["name"], ",", archive)
            if archive:
                idsToArchive.append(c["id"])

        return idsToArchive

if __name__ == "__main__":
    #logger = logging.getLogger()
    #logger.setLevel(logging.DEBUG)
    #logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

    channels = ChannelsList.listChannels()
    print(len(channels), '\n\n\n\n')
    list_channels_to_be_archived(channels)
