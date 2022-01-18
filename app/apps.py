from slack_bolt import App

from . import settings
from .db import Base, engine

Base.metadata.create_all(engine)

app = App(signing_secret=settings.SLACK_SIGNING_SECRET, token=settings.SLACK_BOT_TOKEN)
