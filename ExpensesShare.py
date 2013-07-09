#!/usr/bin/env python
from copy import deepcopy
from flask import Flask
from flask import request
from flask import send_from_directory
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
import config
from ShareCalculator import ShareCalculator


app = Flask(__name__)

client = MongoClient(config.connection_string)
db = client.expensesshare


def convert_to_json(dbObject):
    json_presentation = []
    for doc in dbObject:
        json_presentation.append(doc)
    return json.dumps(json_presentation, default=json_util.default)


@app.route('/user')
def users():
    users = db.users.find()
    return convert_to_json(users)


@app.route('/event')
def events():
    events = db.events.find()
    if events is None:
        return "Events not found", 404
    return convert_to_json(events)


@app.route('/event/<event_id>')
def event_get(event_id):
    event = db.events.find_one({"_id": ObjectId(event_id)})
    if event is None:
        return "Event not found", 404
    participants = []
    for id in event['participants']:
        user = db.users.find_one({"_id": ObjectId(id)})
        participants.append(user)
    del event['participants'][:]
    event['participants'] = participants
    payments = db.payments.find({"event_id": event_id})
    event["payments"] = []

    for payment in payments:
        event['payments'].append(payment)
    for p in event["payments"]:
        payment_participants = deepcopy(p['participants'])
        del p['participants'][:]
        for id in payment_participants:
            user = db.users.find_one({"_id": ObjectId(id)})
            p['participants'].append(user)
        p['payer'] = db.users.find_one({"_id": ObjectId(p['payer'])})
    calculator = ShareCalculator(participants,event['payments'])
    event["Report"] = calculator.Run()
    return json.dumps(event, default=json_util.default)


@app.route('/payment', methods=['POST'])
def create_payment():
    payments = db.payments
    payment = json.loads(request.data)
    # calculation part
    payment['calculation'] = []
    participants_count = len(payment['participants'])
    share = payment['total'] // participants_count
    for participant in payment['participants']:
        payment['calculation'].append({"participant": participant, "share": share})
    payments.insert(payment)
    return "Created", 200


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/<path:fullpath>')
def static_router(fullpath):
    if not fullpath.endswith('.py'):
        return send_from_directory('static', fullpath)
    else:
        return 'thank you!'

if __name__ == '__main__':
    app.run(host=config.ip_address, debug=True)
