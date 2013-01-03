from smartmarks2 import app
import os
# app.run(debug=True)
port = int(os.environ.get('PORT'))
app.run(host='0.0.0.0', port=port)
