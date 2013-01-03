from smartmarks2 import app
import os
# app.run(debug=True)
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
