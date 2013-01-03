from smartmarks2 import app
import os

port = int(os.environ.get('PORT'))
app.run(host='0.0.0.0', port=port)
