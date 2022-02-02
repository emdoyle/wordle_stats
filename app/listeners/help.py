from app.apps import app
from app.blocks import get_help_blocks
from app.regex import HELP_REGEX


@app.message(HELP_REGEX)
def handle_help(say):
    say(blocks=get_help_blocks())
