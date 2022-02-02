from app import settings
from app.apps import app
from app.listeners import *

if __name__ == "__main__":
    app.start(port=settings.DEV_SERVER_PORT, path=settings.SLACK_EVENTS_PATH)
