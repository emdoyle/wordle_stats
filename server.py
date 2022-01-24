from slack_bolt.adapter.socket_mode import SocketModeHandler

from app import settings
from app.apps import app

if __name__ == "__main__":
    SocketModeHandler(app, app_token=settings.SLACK_APP_TOKEN).start()
