"""
Twitter module
Includes the Twitter class and ui interface for testing
"""

import json
from requests import get, RequestException
from requests_oauthlib import OAuth1


class Twitter(object):
    """
    Twitter class.
    Use request method to return time counted pairs of the keyword in
    each users' last N tweets
    """
    CONSUMER_KEY = "nLA0iI2zUQvg01B4jETGGj6wt"
    CONSUMER_SECRET = "2bKLqaBFHW860DAOYDfq66gtr7ge09oa8NmQWFynx2i4zsLGHx"
    TOKEN = "249814405-t3jbE1NIXXz7wZiry0L2RGLBacK7QCaxCMCtMfea"
    TOKEN_SECRET = "1Xe5xqi5lNNL9kN7NqUOG3XHcGgosTYSj8CCAeVA2mFg1"

    BASE_URL = "https://api.twitter.com/1.1/statuses/user_timeline.json"


    @staticmethod
    def _remove_at_symbol(handles):
        return [h[1:] if h[0] == "@" else h for h in handles]

    @classmethod
    def _create_auth_header(cls):
        return OAuth1(
            cls.CONSUMER_KEY,
            cls.CONSUMER_SECRET,
            cls.TOKEN,
            cls.TOKEN_SECRET)

    @staticmethod
    def _create_params(handle, count):
        return {"screen_name": handle, "count": count, "trim_user": "true"}

    @staticmethod
    def _count_instances(raw_tweets, keyword):
        return [[tweet["created_at"], tweet["text"].count(keyword)] for tweet in raw_tweets]

    @classmethod
    def request(cls, handles, keyword, count):
        """
        @param handles: List of twitter handles
        @param keyword: Keyword to search for
        @param count: Number of tweets per handle to search
        """
        handles_without_at = cls._remove_at_symbol(handles)
        auth_header = cls._create_auth_header()
        time_counted_pairs = []

        for handle in handles_without_at:
            try:
                response = get(
                    cls.BASE_URL,
                    params=cls._create_params(handle, count),
                    auth=auth_header)

                if response.status_code != 200:
                    raise RequestException(response.status_code)

                raw_tweets = json.loads(response.text)
                time_counted_pairs.extend(cls._count_instances(raw_tweets, keyword))

            except RequestException as err:
                print(err)

        return time_counted_pairs

if __name__ == "__main__":
    HANDLES = raw_input("Please enter a list of twitter handles separated by spaces: ").split()
    KEYWORD = raw_input("Please enter keyword or hashtag: ")
    COUNT = raw_input("Please enter the number of tweets to search for: ")

    TIME_COUNTED_PAIRS = Twitter.request(HANDLES, KEYWORD, COUNT)
    TOTAL_OCCURANCES = sum(tcp[1] for tcp in TIME_COUNTED_PAIRS)
    print([TOTAL_OCCURANCES, TIME_COUNTED_PAIRS])
