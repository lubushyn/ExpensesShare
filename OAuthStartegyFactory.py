__author__ = 'aliubushyn'
from flask_oauth import OAuth
from TwitterStrategy import TwitterStrategy


class OAuthStrategyFactory:
    def __init__(self):
        self.oauth = OAuth()
        self.twitterStrategy = TwitterStrategy(self.oauth)

    def twitter(self):
        return self.twitterStrategy.twitter