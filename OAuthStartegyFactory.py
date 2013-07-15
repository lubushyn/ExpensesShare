__author__ = 'aliubushyn'
from flask_oauth import OAuth
from TwitterStrategy import TwitterStrategy
from FacebookStrategy import FacebookStrategy

class OAuthStrategyFactory:
    def __init__(self):
        self.oauth = OAuth()
        self.twitterStrategy = TwitterStrategy(self.oauth)
        self.facebookStrategy = FacebookStrategy(self.oauth)

    def twitter(self):
        return self.twitterStrategy.twitter

    def facebook(self):
        return  self.facebookStrategy.facebook