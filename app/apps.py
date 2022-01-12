from slack_bolt import App

from . import settings


app = App(
    signing_secret=settings.SLACK_SIGNING_SECRET,
    token=settings.SLACK_BOT_TOKEN
)
