import os
import logging
from slack import WebClient
from slack.errors import SlackApiError
import time
import ssl as ssl_lib
import certifi

class ChannelsList:
    slack_web_client = None

    def __init__(self):
        # Initialize a Web API client
        self.slack_web_client = WebClient(token=os.environ['SLACK_USER_TOKEN'],ssl=True)

    #@app.route('/slack/channels/clean')
    def list_channels(self):

        response = self.slack_web_client.conversations_list(
            types="public_channel",
            exclude_archived="true",
            limit=200
        )
        channels = response["channels"]
        response_metadata = response["response_metadata"]

        while "next_cursor" in response_metadata and response_metadata["next_cursor"]:
            response = self.slack_web_client.conversations_list(
                types="public_channel",
                exclude_archived="true",
                limit=200,
                cursor=response_metadata["next_cursor"]
            )
            channels += response["channels"]

            response_metadata = response["response_metadata"]

        return channels

    def list_channels_to_be_archived(self, inactive_days):
        oldest = time.time() - inactive_days*24*60*60
        channels = self.list_channels()
        #channels = [{"id":"C012LEEVBAT", "name":"ameno-tati"}]
        idsToArchive = []
        for c in channels:
            if c["created"] > oldest:
                print(c["id"], ",", c["name"], ", False")
                continue

            response_hst = self.slack_web_client.conversations_history(
                channel=c["id"],
                oldest=str(oldest)
            )
            messages = response_hst["messages"]
            valid_subtypes = ["bot_message", "message_replied", "thread_broadcast"]

            archive=True
            for m in messages:
                if "bot_profile" in m and m["bot_profile"]["app_id"] == "A011U6B341Y":
                    continue
                
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

    channelList = ChannelsList()
    print(channelList.list_channels_to_be_archived(60))
