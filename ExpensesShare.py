#!/usr/bin/env python
from flask import Flask
from flask import request, redirect
from flask import send_from_directory
from flask import session
from flask import g
from flask_login import LoginManager, \
    login_required, login_user, \
    logout_user, user_unauthorized
from pymongo import MongoClient
from bson import json_util, ObjectId
from User import User
import json
from ShareCalculator import ShareCalculator
from OAuthStartegyFactory import OAuthStrategyFactory
import config

app = Flask(__name__)
app.secret_key = "wkdsfgsdfgsdfegrkqkerklqwgerjfdsdf"

client = MongoClient(config.MONGODB_URL)
db = client[config.DB_NAME]
factory = OAuthStrategyFactory(db)

twitter = factory.twitter()
facebook = factory.facebook()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main'
@login_manager.user_loader
def load_user(user_id):
    db_user =  db.users.find_one({'_id': ObjectId(user_id)})
    if db_user is not None:
        if db_user['facebook']:
            return User(email=db_user['email'], id=str(db_user['_id']), name=db_user['name'])
        if db_user['twitter']:
            return User(name=db_user['username'])

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = db.users.find_one({"_id":ObjectId(session['user_id'])})

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@facebook.tokengetter
def get_facebook_token(token=None):
    user = g.user
    #if user is not None:
    #    return user['facebook_access_token']
    #user = g.user
    return session.get('facebook_token')


def jsonify(dbObject):
    json_presentation = []
    for doc in dbObject:
        json_presentation.append(doc)
    return json.dumps(json_presentation, default=json_util.default)


@app.route('/user')
@login_required
def users():
    users = db.users.find()
    return jsonify(users)


@app.route('/event')
@login_required
def events():
    events = db.events.find()
    if events is None:
        return "Events not found", 404
    return jsonify(events)


@app.route('/event/<event_id>')
@login_required
def get_event(event_id):
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if event is None:
        return "Event not found", 404
    result = dict(event)
    participants = map(ObjectId, result['participants'])
    people = db.users.find({"_id": {"$in": participants}})
    result['participants'] = [dict(id=str(user['_id']), name=user['name'])
                              for user in people]

    calculator = ShareCalculator(result['participants'], event['payments'])
    result["report"] = calculator.Run()
    return json.dumps(result, default=json_util.default)


@app.route('/event/<event_id>', methods=['PATCH'])
@login_required
def create_payment(event_id):
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if event is None:
        return "Event not found", 404

    # TODO: validate
    # {payer: "id", participants: [...], total: 123}
    payment = json.loads(request.data)
    share = round(float(payment['total']) / float(len(payment['participants'])), 2)
    payment['calculation'] = [dict(participant=user, share=share)
                              for user in payment['participants']]
    db.events.update({"_id": ObjectId(event_id)},
                     {"$push": {"payments": payment}})

    return "Created", 200

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/')

@app.route('/app')
@login_required
def root():
    return app.send_static_file('index.html')


@app.route('/')
def main():
    return app.send_static_file('main.html')


@app.route('/login')
def login():
    type = request.args.get('type', '')
    if type == "facebook":
        return factory.facebookStrategy.login()
    if type == "twitter":
        return factory.twitterStrategy.login()


@app.route('/oauth-authorized-twitter')
@twitter.authorized_handler
def oauth_authorized_twitter(resp):
    return factory.twitterStrategy.authorized(resp)


@app.route('/oauth-authorized-facebook')
@facebook.authorized_handler
def oauth_authorized_facebook(resp):
    return factory.facebookStrategy.authorized(resp)


@app.route('/<path:fullpath>')
def static_router(fullpath):
    if not fullpath.endswith('.py'):
        return send_from_directory('static', fullpath)
    else:
        return 'thank you!'


if __name__ == '__main__':
    app.run(host=config.IP_ADDRESS, debug=True)
