from app import app, settings
from slack_bolt.adapter.socket_mode import SocketModeHandler


if __name__ == "__main__":
    SocketModeHandler(app, settings.SLACK_APP_TOKEN).start()
