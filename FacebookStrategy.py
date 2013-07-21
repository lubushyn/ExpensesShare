__author__ = 'aliubushyn'
from flask import request
from flask import url_for
from flask import session
from flask import flash
from flask import redirect
from flask import g


class FacebookStrategy:
    def __init__(self, oauth, db):
        self.facebook = oauth.remote_app('facebook',
                                         base_url='https://graph.facebook.com/',
                                         request_token_url=None,
                                         access_token_url='/oauth/access_token',
                                         authorize_url='https://www.facebook.com/dialog/oauth',
                                         consumer_key="321923181229609",
                                         consumer_secret="532b839ed2c4c4469e6752c32ac057fe",
                                         request_token_params={'scope': 'email'}
        )
        self.db = db


    def authorized(self, resp):
        next_url = request.args.get('next') or url_for('app')
        if resp is None:
            flash(u'You denied the request to sign in.')
            return redirect(next_url)

        session['access_token'] = resp['access_token']
        session['expires'] = resp['expires']
        session['facebook_token'] = resp['access_token']
        me = self.facebook.get('/me')
        user = self.db.users.find_one({"email": me.data["email"]})
        if user is None:
            self.db.users.insert({"username": me.data["username"],
                                  "is_authenticated": True,
                                  "name": me.data["name"], "email": me.data["email"],
                                  "facebook": True, "twitter": False, "facebook_access_token": resp["access_token"],
                                  "facebook_expires": resp["expires"]})
        db_user = self.db.users.find_one({"email": me.data["email"]})
        session['user_id'] = str(db_user['_id'])
        g.user = db_user
        return redirect(next_url)


    def login(self):
        url = url_for('oauth_authorized_facebook',
                      next=request.args.get('next') or request.referrer + "app" or None, _external=True)
        return self.facebook.authorize(callback=url)