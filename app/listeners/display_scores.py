from typing import Dict

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.apps import app
from app.blocks import get_error_block
from app.constants import WORDLE_FAIL_INDICATOR, WORDLE_MAX_ATTEMPTS
from app.dataclasses.users import UserMention
from app.db import Score, User, get_engine


def get_individual_scores(team_id: str, user_mention: "UserMention") -> Dict:
    with Session(get_engine(team_id=team_id)) as session:
        try:
            average_attempts = session.execute(
                select(
                    func.avg(Score.attempts),
                )
                .join(User.scores)
                .group_by(User.id)
                .where(User.slack_id == user_mention.slack_id)
            ).first()[0]
            if average_attempts is not None:
                average_attempts = round(average_attempts, 2)
            recent_attempts = session.execute(
                select(Score.edition, Score.attempts)
                .join(User.scores)
                .where(User.slack_id == user_mention.slack_id)
                .order_by(desc(Score.edition))
                .limit(5)
            ).all()
            return {
                "average_attempts": average_attempts,
                "recent_attempts": recent_attempts,
            }
        except TypeError:
            # Handle no scores found
            return {}


def display_user_scores(team_id: str, user_mention: "UserMention") -> str:
    user_scores = get_individual_scores(team_id=team_id, user_mention=user_mention)
    header = f"{user_mention.encoded} (Avg: {user_scores.get('average_attempts')})"
    recent_rows = "\n".join(
        (
            f"Wordle {score[0]}: {score[1] or WORDLE_FAIL_INDICATOR}/{WORDLE_MAX_ATTEMPTS}"
            for score in user_scores.get("recent_attempts", [])
        )
    )
    return "\n".join((header, recent_rows))


@app.command("/scores")
def handle_scores_command(ack, respond, command, logger):
    logger.debug("handle_scores_command called")
    ack()
    team_id = command["team_id"]
    items = command["text"].strip().split()
    try:
        user_mentions = map(UserMention.parse, items)
        response_text = "\n\n".join(
            (
                display_user_scores(team_id, user_mention)
                for user_mention in user_mentions
            )
        )
    except ValueError as e:
        logger.exception("Error displaying scores")
        respond(blocks=[get_error_block(error=e)])
        return
    if not response_text:
        respond(text="Usage: /scores @user1 [@user2 ...]")
    logger.info("Display scores: %s", response_text)
    respond(text=response_text)
