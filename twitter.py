import json
from pyramda import pick
from requests import get, RequestException
from requests_oauthlib import OAuth1


class Twitter:
    """
    Twitter class.
    Use request method to call
    """
    CONSUMER_KEY="nLA0iI2zUQvg01B4jETGGj6wt"
    CONSUMER_SECRET="2bKLqaBFHW860DAOYDfq66gtr7ge09oa8NmQWFynx2i4zsLGHx"
    TOKEN="249814405-t3jbE1NIXXz7wZiry0L2RGLBacK7QCaxCMCtMfea"
    TOKEN_SECRET="1Xe5xqi5lNNL9kN7NqUOG3XHcGgosTYSj8CCAeVA2mFg1"

    BASE_URL="https://api.twitter.com/1.1/statuses/user_timeline.json"


    @staticmethod
    def _remove_at_symbol(handles):
        return [h[1:] if h[0] =="@" else h for h in handles]

    @classmethod
    def _create_auth_header(cls):
        return OAuth1(
            cls.CONSUMER_KEY,
            cls.CONSUMER_SECRET,
            cls.TOKEN,
            cls.TOKEN_SECRET)

    @staticmethod
    def _create_params(handle, n):
        return {"screen_name": handle, "count": n, "trim_user": "true"}

    @staticmethod
    def _count_instances(stripped_tweets, keyword):
        return [[tweet["created_at"], tweet["text"].count(keyword)] for tweet in stripped_tweets]

    @classmethod
    def request(cls, handles, keyword, n):
        handles_without_at = cls._remove_at_symbol(handles)
        auth_header = cls._create_auth_header()
        time_counted_pairs = []

        for handle in handles_without_at:
            try:
                response = get(
                    cls.BASE_URL,
                    params=cls._create_params(handle, n),
                    auth=auth_header)

                if response.status_code != 200:
                    raise RequestException

            except RequestException as e:
                print(e)
                continue

            raw_tweets = json.loads(response.text)
            stripped_tweets = map(pick(["text", "created_at"]), raw_tweets)
            time_counted_pairs.extend(cls._count_instances(stripped_tweets, keyword))

        return time_counted_pairs

if __name__ == "__main__":
    handles = raw_input("Please enter a list of twitter handles separated by spaces: ").split()
    keyword = raw_input("Please enter keyword or hashtag: ")
    n = raw_input("Please enter the number of tweets to search for: ")

    time_counted_pairs = Twitter.request(handles, keyword, n)
    total = sum(map(lambda x: x[1], time_counted_pairs))
    print([total, time_counted_pairs])
