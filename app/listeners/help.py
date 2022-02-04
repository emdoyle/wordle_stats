from app.apps import app
from app.blocks import get_help_blocks
from app.regex import HELP_REGEX


@app.message(HELP_REGEX)
def handle_help(client, message, logger):
    logger.debug("handle_help called")
    logger.info("Showing help for user: %s", message.get("user", "(unknown)"))
    client.chat_postEphemeral(
        channel=message["channel"], user=message["user"], blocks=get_help_blocks()
    )
