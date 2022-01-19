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

    try:
        username = body["user"]["username"]
        raw_score = action["value"]
    except KeyError:
        # TODO: logger
        respond(
            text="Could not submit score :( Please try again later!",
            response_type="ephemeral",
            replace_original=True,
        )
        return

    with Session(engine) as session:
        try:
            user = session.execute(
                select(User).where(User.username == username)
            ).first()[0]
        except (TypeError, IndexError):
            user = User(username=username)
            session.add(user)

        try:
            wordle_score = WordleScore.parse(raw_score=raw_score)
            wordle_score.validate(raise_error=True)
        except ValueError as e:
            respond(
                blocks=[
                    asdict(
                        PlainTextSection(
                            text=PlainTextBlock(
                                text=(
                                    "Click the 'Share' button on your Wordle screen "
                                    "and paste from your clipboard below!"
                                ),
                                emoji=True,
                            )
                        )
                    ),
                    asdict(
                        MultiLineTextInputBlock(
                            label=PlainTextLabel(
                                text=":clipboard: Paste your score here:", emoji=True
                            ),
                            element=PlainTextInput(
                                multiline=True, action_id="submit_score"
                            ),
                        )
                    ),
                    asdict(
                        PlainTextSection(
                            text=PlainTextBlock(
                                text=f"Error: {e}",
                                emoji=True,
                            )
                        )
                    ),
                ],
                response_type="ephemeral",
                replace_original=True,
            )
            return

        session.add(
            Score(
                user=user,
                edition=wordle_score.edition,
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
