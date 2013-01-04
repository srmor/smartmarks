from flask import Flask
from flask.ext.mongoengine import MongoEngine
import os
app = Flask(__name__)

app.config["MONGODB_DB"] = os.environ["MONGODB_DB"]
app.config["MONGODB_USERNAME"] = os.environ["MONGODB_USERNAME"]
app.config["MONGODB_PASSWORD"] = os.environ["MONGODB_PASSWORD"]
app.config["MONGODB_HOST"] = os.environ["MONGODB_HOST"]
app.config["MONGODB_PORT"] = os.environ["MONGODB_PORT"]
app.config["SECRET_KEY"] = "(\x9f\x050\xc0\x1f\x0cn\x1eD\xb8\xc9\xfb\xcd]\xb9\x82@\x8d\xa1\xcc\x0fqw"

db = MongoEngine(app)

import smartmarks.views
import smartmarks.api_views
