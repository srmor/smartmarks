from flask import Flask
from flask.ext.mongoengine import MongoEngine
app = Flask(__name__)
app.config["SECRET_KEY"] = "(\x9f\x050\xc0\x1f\x0cn\x1eD\xb8\xc9\xfb\xcd]\xb9\x82@\x8d\xa1\xcc\x0fqw"

db = MongoEngine(app)

import smartmarks2.views
import smartmarks2.api_views
