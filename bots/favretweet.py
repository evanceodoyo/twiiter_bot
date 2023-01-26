#!/usr/bin/python3
"""
Uses Tweepy stream to actively watch for tweets that contain certain keywords.
For each tweet, if you are not the tweet author, it will marked the tweet as `liked` and then retweet it.
Useful  to feed your account with content relevant to your interests.
"""

import tweepy
import logging
from config import create_api
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class FaveRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        # Ignore reply or tweet by me.
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            return

        if not tweet.favorited:
            # Mark the tweet as liked.
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)

        if not tweet.retweeted:
            # Retweet the tweet.
            try:
                tweet.retweet()
            except Exception as e:
                logging.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)


def main(keywords):
    api = create_api()
    tweets_listener = FaveRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=['en'])


if __name__ == '__main__':
    main(['Python', 'Django', 'JavaScript', 'HTML',
         'CSS', 'Docker', 'Golang', 'Rust',])
