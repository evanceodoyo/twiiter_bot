#!/usr/bin/python3
"""
Uses Tweepy API to get a list of your followers after 1 minute.
Checks if you are already follower each user, if not, it follows back the user.
"""

import tweepy
import logging
from config import create_api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def follow_followers(api):
    logger.info("Retrieving the followers")
    for follower in tweepy.Cursor(api.follower).items():
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()


def main():
    api = create_api()
    while True:
        follow_followers(api)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == '__main__':
    main()
