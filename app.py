import settings
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


app = App(
    signing_secret=settings.SLACK_SIGNING_SECRET,
    token=settings.SLACK_BOT_TOKEN
)

if __name__ == "__main__":
    SocketModeHandler(app, settings.SLACK_APP_TOKEN).start()