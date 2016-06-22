# Starts waitress server (wsgisrv) on the localhost
from waitress import serve
import app
wsgiapp = app.api
serve(wsgiapp, host='0.0.0.0', port=8888)

