from app.apps import app
from app.blocks import get_help_blocks
from app.regex import HELP_REGEX


@app.event("app_mention")
def handle_mention(body, say):
    event = body["event"]
    if HELP_REGEX.match(event["text"]):
        say(blocks=get_help_blocks())
        return
