import re
from dataclasses import asdict
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..apps import app
from ..dataclasses import (
    MultiLineTextInputBlock,
    PlainTextBlock,
    PlainTextInput,
    PlainTextLabel,
    PlainTextSection,
)
from ..dataclasses.scores.base import WordleScore
from ..db import Score, User, engine


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
def handle_wordle_score(ack, action, respond, body):
    ack()

    def fail():
        respond(
            text="Could not submit score :( Please try again later!",
            response_type="ephemeral",
            replace_original=True,
        )

    try:
        username = body["user"]["username"]
        raw_score = action["value"]
    except KeyError:
        # TODO: logger
        fail()
        return

    with Session(engine) as session:
        try:
            user = session.execute(
                select(User).where(User.username == username)
            ).first()[0]
        except (TypeError, IndexError):
            user = User(username=username)
            session.add(user)

        wordle_score = WordleScore.parse(raw_score=raw_score)
        # TODO: date could be based on the edition... or could just store the edition instead of date
        session.add(
            Score(
                user=user,
                date=date.today(),
                attempts=wordle_score.attempts,
                raw=raw_score,
            )
        )
        session.commit()

    respond(
        text=":sparkles: Score submitted!",
        response_type="ephemeral",
        replace_original=True,
    )


@app.message("hello")
def weird(say):
    say("weird...")
