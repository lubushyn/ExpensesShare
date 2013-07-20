__author__ = 'aliubushyn'
from flask import request
from flask import url_for
from flask import session
from flask import flash
from flask import redirect


class TwitterStrategy:
    def __init__(self, oauth, db):
        self.twitter = oauth.remote_app('twitter',
                                        base_url='https://api.twitter.com/1/',
                                        request_token_url='https://api.twitter.com/oauth/request_token',
                                        access_token_url='https://api.twitter.com/oauth/access_token',
                                        authorize_url='https://api.twitter.com/oauth/authenticate',
                                        consumer_key='0LbXly2JdkuezCN8FrhOw',
                                        consumer_secret='YK8amhp3t2lTpHf32N3k8g1tukoZ4AkJaYia3cI4')
        self.db = db

    def authorized(self, resp):
        next_url = request.args.get('next') or url_for('app')
        if resp is None:
            flash(u'You denied the request to sign in.')
            return redirect(next_url)

        session['twitter_token'] = (
            resp['oauth_token'],
            resp['oauth_token_secret']
        )
        session['twitter_user'] = resp['screen_name']
        user = self.db.users.find_one({"twitter_screen_name": resp['screen_name']})
        if user is None:
            self.db.users.insert({"username": resp['screen_name'],
                                  "twitter": True, "facebook": False, "twitter_access_token": resp["oauth_token"],
                                  "twitter_oauth_token_secret": resp["oauth_token_secret"]})
        db_user = self.db.users.find_one({"username": resp['screen_name']})
        session['user_id'] = str(db_user['_id'])
        flash('You were signed in as %s' % resp['screen_name'])
        return redirect(next_url)

    def login(self):
        return self.twitter.authorize(callback=url_for('oauth_authorized_twitter',
                                                       next=request.args.get(
                                                           'next') or request.referrer + "app" or None))