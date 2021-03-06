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
    user = g.user
    if user is not None:
        if('twitter_access_token' in user.keys() and 'twitter_oauth_token_secret' in user.keys()):
            return user['twitter_access_token'], user['twitter_oauth_token_secret']
    return session.get('twitter_oauthtok')


@facebook.tokengetter
def get_facebook_token(token=None):
    user = g.user
    if user is not None:
        if 'facebook_access_token' in user.keys():
            return user['facebook_access_token'], ''
    #user = g.user
    return session.get('facebook_token'), ''


def jsonify(dbObject):
    json_presentation = []
    for doc in dbObject:
        json_presentation.append(doc)
    return json.dumps(json_presentation, default=json_util.default)

# TODO fix it somebody - we have to problems
# 1. user id and participant id is not consistant (as me - I explain)
@app.route('/user/me') 
# @login_required
def user():
    # array wrap - it is hack for jsonify, shoud be rewrited
    return json.dumps(g.user,default=json_util.default)
    

@app.route('/user')
# @login_required
def users():
    users = db.users.find()
    return jsonify(users)

@app.route('/user', methods=['POST'])
# @login_required
def create_user():
    new_user = json.loads(request.data)
    res = db.users.insert({"name":new_user["name"]})
    return json.dumps(res,default=json_util.default), 200


@app.route('/event')
# @login_required
def events():
    events = db.events.find()
    if events is None:
        return "Events not found", 404
    return jsonify(events)


@app.route('/event/<event_id>', defaults={'limit':  None, 'offset': None})
@app.route('/event/<event_id>/<limit>', defaults={'offset': 0})
@app.route('/event/<event_id>/<limit>/<offset>')
# @login_required
def get_event(event_id, limit, offset):
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if event is None:
        return "Event not found", 404
    result = dict(event)
    
    if limit is None and offset is None:
        result["payments"] = result["payments"]
    elif limit is not None:
        result["payments"] = result["payments"][-int(limit):]
    else:
        result["payments"] = result["payments"][int(offset):int(limit)]
    
    participants = map(ObjectId, result['participants'])
    people = db.users.find({"_id": {"$in": participants}})
    result['participants'] = [dict(id=str(user['_id']), name=user['name'])
                              for user in people]

    calculator = ShareCalculator(result['participants'], event['payments'])
    result["report"] = calculator.Run()
    return json.dumps(result, default=json_util.default)


@app.route('/event/<event_id>', methods=['PATCH'])
# @login_required
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


@app.route('/event/<event_id>/user', methods=['PATCH'])
# @login_required
def add_user(event_id):
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if event is None:
        return "Event not found", 404
    new_user = json.loads(request.data)
    db.events.update({"_id": ObjectId(event_id)},
                     {"$push": {"participants": new_user["id"]}})
    return "Done", 200

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/')

@app.route('/app')
# @login_required
def root():
    return app.send_static_file('index.html')


@app.route('/')
def main():
    return redirect('/app')
    # return app.send_static_file('main.html')


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


@app.route('/report/<event_id>')
# @login_required
def get_report(event_id):
    report = db.events.aggregate([
        {"$match":{"_id":ObjectId(event_id)}},
        {"$unwind": "$payments"},
        {"$group": {"_id": "$payments.date", "total": {"$sum": "$payments.total"}}},
        {"$sort": { "_id": 1 } }
    ])

    return json.dumps(report['result'], default=json_util.default)

@app.route('/report/<event_id>/<participant_id>')
# @login_required
def get_report_by_participant(event_id, participant_id):
    # TODO lol, mongodb INJECTION HERE
    report = db.events.aggregate([
        {"$match":{"_id":ObjectId(event_id)}},
        {"$project":{"payments":1}}, 
        {"$unwind": "$payments"}, 
        {"$match":{'payments.participants': participant_id}},
        {"$project":{'payments.date':1,'payments.calculation':1}}, 
        {"$unwind":'$payments.calculation'},
        {"$match":{'payments.calculation.participant': participant_id}},
        {"$group":{"_id": "$payments.date", "total": {"$sum": "$payments.calculation.share"}}},
        {"$sort":{"_id":1}}
    ])

    return json.dumps(report['result'], default=json_util.default)

@app.route('/<path:fullpath>')
def static_router(fullpath):
    if not fullpath.endswith('.py'):
        return send_from_directory('static', fullpath)
    else:
        return 'thank you!'


if __name__ == '__main__':
    app.run(host=config.IP_ADDRESS, debug=True)
