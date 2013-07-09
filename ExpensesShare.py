from flask import Flask
from flask import request
from flask import render_template
from pymongo import MongoClient
from bson import json_util, ObjectId
from copy import deepcopy
import config
import json

app = Flask(__name__)

client = MongoClient(config.connection_string)
db = client.expensesshare



def convert_to_json(dbObject):
    json_presentation = []
    for doc in dbObject:
        json_presentation.append(doc)
    return json.dumps(json_presentation, default=json_util.default)


@app.route('/')
def index():
    return render_template('index.html')


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
        participants = deepcopy(p['participants'])
        del p['participants'][:]
        for id in participants:
            user  = db.users.find_one({"_id": ObjectId(id)})
            p['participants'].append(user)
        p['payer'] = db.users.find_one({"_id": ObjectId(p['payer'])})
    #Extend payer Id to user object
    return json.dumps(event, default=json_util.default)

@app.route('/payment',methods=['POST'])
def create_payment():
    payments = db.payments
    payment = json.loads(request.data)
    payments.insert(payment)
    return "Created", 200

if __name__ == '__main__':
    app.run(host=config.ip_address, debug=True)
