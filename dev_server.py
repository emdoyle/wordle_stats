from slack_bolt.adapter.socket_mode import SocketModeHandler

from app import settings
from app.apps import app
from app.listeners import *

if __name__ == "__main__":
    SocketModeHandler(app, app_token=settings.SLACK_APP_TOKEN).connect()
    app.start(port=settings.DEV_SERVER_PORT)
