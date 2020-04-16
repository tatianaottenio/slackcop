import os
import logging
from slack import WebClient
import time
import ssl as ssl_lib
import certifi
from onboarding_tutorial import OnboardingTutorial

# Initialize a Web API client
slack_web_client_bot = WebClient(token='xoxb-101787336466-1055493452038-xgxAudSgWsbpNZqUSHaM3TIp',ssl=True)

def channels_archive(channels):
    for id in channels:
        print("========",id)
        response_join = slack_web_client_bot.conversations_join(
            channel=id
        )
        if response_join["ok"]:
            print("join", response_join["ok"])
            response_arch = slack_web_client_bot.conversations_archive(
                channel=id
            )
            if response_arch["ok"]:
                print("archive", response_arch["ok"])
            else:
                print("archive", response_arch["error"])
        else:
            print("join", response_join["error"])
        print("========")

if __name__ == "__main__":
    #logger = logging.getLogger()
    #logger.setLevel(logging.DEBUG)
    #logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    #channels = channels_list()
    #print(len(channels), '\n\n\n\n')
    #channels_archive(channels)
    channels = ["CMEETRCFK"]
    #channels = ["C011WR1QZQS"]
    channels_archive(channels)
