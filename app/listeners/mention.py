from app.apps import app
from app.blocks import get_tutorial_blocks


@app.event("app_mention")
def handle_mention(client, body):
    event = body["event"]
    # For now, since no mention actions, just show tutorial every time
    client.chat_postEphemeral(
        channel=event["channel"], user=event["user"], blocks=get_tutorial_blocks()
    )
