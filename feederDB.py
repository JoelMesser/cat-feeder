from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from gpiozero import Button
from threading import Thread
import datetime
import os

def resetButtonLoop():
  button = Button(2)

  while(True):
    button.wait_for_press()
    reloadFeeder("Button")

PERCENT_PER_FEEDING = 7
FEEDER = 'joel'

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'feederDB.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
resetButtonThread = Thread(target = resetButtonLoop)
resetButtonThread.start()

class FeedEntry(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  name = db.Column(db.String(40))
  remaining = db.Column(db.Integer)

  def __init__(self, name, remaining):
    self.name = name
    self.remaining = remaining

class FeedEntrySchema(ma.Schema):
  class Meta:
    fields = ('id', 'time', 'name', 'remaining')

feed_schema = FeedEntrySchema()
feed_entries_schema = FeedEntrySchema(many=True)

@app.route("/feedings", methods=["GET"])
def getFeedings():
  all_feedings = FeedEntry.query.all()
  result = feed_entries_schema.dump(all_feedings)
  return jsonify(result.data)

@app.route('/logFeeding', methods=["POST"])
def flaskLogFeeding():
  user = request.headers.get('X-SSL-CERT')
  logFeeding(user)

@app.route('/reloadFeeder', methods=['POST'])
def flaskReloadFeeder():
  user = request.headers.get('X-SSL-CERT')
  reloadFeeder(user)

def reloadFeeder(user):
  newFeeding = FeedEntry(FEEDER, 100)
  db.session.add(newFeeding)
  db.session.commit()

def logFeeding(user):  
  lastFeeding = FeedEntry.query.all().one_or_none()
  remaining = max(lastFeeding.remaining - PERCENT_PER_FEEDING, 0)
  newFeeding = FeedEntry(FEEDER, remaining)
  db.session.add(newFeeding)
  db.session.commit()

  return jsonify(newFeeding)
