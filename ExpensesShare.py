#!/usr/bin/env python
from flask import Flask
from flask import request
from flask import send_from_directory
from flask import session
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
from ShareCalculator import ShareCalculator
from OAuthStartegyFactory import OAuthStrategyFactory
import config

app = Flask(__name__)
app.secret_key = "wkdsfgsdfgsdfegrkqkerklqwgerjfdsdf"

client = MongoClient(config.MONGODB_URL)
db = client[config.DB_NAME]
factory = OAuthStrategyFactory()
twitter = factory.twitter()


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


def jsonify(dbObject):
    json_presentation = []
    for doc in dbObject:
        json_presentation.append(doc)
    return json.dumps(json_presentation, default=json_util.default)


@app.route('/user')
def users():
    users = db.users.find()
    return jsonify(users)


@app.route('/event')
def events():
    events = db.events.find()
    if events is None:
        return "Events not found", 404
    return jsonify(events)


@app.route('/event/<event_id>')
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


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/login')
def login():
    return factory.twitterStrategy.login()


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    return factory.twitterStrategy.authorized(resp)


@app.route('/<path:fullpath>')
def static_router(fullpath):
    if not fullpath.endswith('.py'):
        return send_from_directory('static', fullpath)
    else:
        return 'thank you!'


if __name__ == '__main__':
    app.run(host=config.IP_ADDRESS, debug=True)
