import re
from dataclasses import asdict

from ..apps import app
from ..dataclasses import (
    MultiLineTextInputBlock,
    PlainTextBlock,
    PlainTextInput,
    PlainTextLabel,
    PlainTextSection,
)


@app.message(re.compile(r"\bsubmit score\b", re.IGNORECASE))
def handle_score_submission(client, payload):
    client.chat_postEphemeral(
        channel=payload["channel"],
        user=payload["user"],
        text="Share your Wordle score",
        blocks=[
            asdict(
                PlainTextSection(
                    text=PlainTextBlock(
                        text="Click the 'Share' button on your Wordle screen and paste from your clipboard below!",
                        emoji=True,
                    )
                )
            ),
            asdict(
                MultiLineTextInputBlock(
                    label=PlainTextLabel(
                        text=":clipboard: Paste your score here:", emoji=True
                    ),
                    element=PlainTextInput(multiline=True, action_id="submit_score"),
                )
            ),
        ],
    )


@app.action("submit_score")
def handle_wordle_score(ack, action, respond):
    ack()
    respond(
        text=":sparkles: Score submitted!",
        response_type="ephemeral",
        replace_original=True,
    )


@app.message("hello")
def weird(say):
    say("weird...")
