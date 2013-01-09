from flask import Flask
from flask.ext.mongoengine import MongoEngine
import os
app = Flask(__name__)

app.config["MONGODB_DB"] = os.environ["MONGODB_DB"]
app.config["MONGODB_USERNAME"] = os.environ["MONGODB_USERNAME"]
app.config["MONGODB_PASSWORD"] = os.environ["MONGODB_PASSWORD"]
app.config["MONGODB_HOST"] = os.environ["MONGODB_HOST"]
app.config["MONGODB_PORT"] = os.environ["MONGODB_PORT"]
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

db = MongoEngine(app)

from smartmarks.fxns import getCss, getJs, getImg
app.jinja_env.globals.update(getCss=getCss, getJs=getJs, getImg=getImg)

import smartmarks.views
import smartmarks.api_views
