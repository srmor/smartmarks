from smartmarks2 import app

app.config["MONGODB_DB"] = "smartmarks"
app.run(debug=True)
