from smartmarks2 import app
import os

app.config["MONGODB_DB"] = "heroku_app10619800"
app.config["MONGODB_USERNAME"] = "heroku_app10619800"
app.config["MONGODB_PASSWORD"] = "p4grl2jfla4ncd22724husetgg"
app.config["MONGODB_HOST"] = "ds047197.mongolab.com"
app.config["MONGODB_PORT"] = 47197

port = int(os.environ.get('PORT'))
app.run(host='0.0.0.0', port=port)
