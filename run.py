import os
from app import app

port = int(os.getenv('PORT', 5000))

app.run(host='0.0.0.0', port=port, debug = True)
