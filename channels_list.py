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
        slack_web_client_tati = WebClient(token='xoxp-101787336466-724089578480-1063515502325-7d9f1b7ae416f45dc4112799eb0a8454',ssl=True)
        
        response = slack_web_client_tati.conversations_list(
            types="public_channel",
            exclude_archived="true",
            limit=200
        )
        channels = response["channels"]
        response_metadata = response["response_metadata"]

        while "next_cursor" in response_metadata and response_metadata["next_cursor"]:
            response = slack_web_client_tati.conversations_list(
                types="public_channel",
                exclude_archived="true",
                limit=200,
                cursor=response_metadata["next_cursor"]
            )
            channels += response["channels"]

            response_metadata = response["response_metadata"]

        return channels
