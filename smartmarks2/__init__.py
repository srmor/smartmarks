from flask import Flask
from flask.ext.mongoengine import MongoEngine
app = Flask(__name__)
# app.config["MONGODB_DB"] = "smartmarks"
app.config["MONGODB_DB"] = "heroku_app10619800"
app.config["MONGODB_USERNAME"] = "heroku_app10619800"
app.config["MONGODB_PASSWORD"] = "p4grl2jfla4ncd22724husetgg"
app.config["MONGODB_HOST"] = "ds047197.mongolab.com"
app.config["MONGODB_PORT"] = 47197
app.config["SECRET_KEY"] = "(\x9f\x050\xc0\x1f\x0cn\x1eD\xb8\xc9\xfb\xcd]\xb9\x82@\x8d\xa1\xcc\x0fqw"

db = MongoEngine(app)

import smartmarks2.views
import smartmarks2.api_views
