from app.apps import app
from app.blocks import get_help_blocks
from app.regex import HELP_REGEX


@app.event("app_mention")
def handle_mention(client, body):
    event = body["event"]
    if HELP_REGEX.match(event["text"]):
        client.chat_postEphemeral(
            channel=event["channel"], user=event["user"], blocks=get_help_blocks()
        )
        return
