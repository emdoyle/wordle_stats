from datetime import datetime, timedelta, timezone

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.apps import app
from app.constants import WORDLE_MAX_ATTEMPTS
from app.dataclasses.users import UserMention
from app.db import Score, User, get_engine
from util.channels import get_member_channel_ids
from util.tasks import daily_task
from util.teams import installed_team_ids
from util.timezone import PACIFIC_TIME, get_timezone_for_team

EMOJI_PLACEMENTS = [
    ":first_place_medal:",
    ":second_place_medal:",
    ":third_place_medal:",
]


def generate_winners_message(team_id: str) -> str:
    # - TODO: unique constraint for (user_id, edition) on Score, handle this in submission
    # Wordle [edition] has concluded! Congratulations to podium finishers :tada:
    #
    # :first_place_medal: (user_mentions)
    # :second_place_medal: (user_mentions)
    # :third_place_medal: (user_mentions)
    team_timezone = get_timezone_for_team(app=app, team_id=team_id) or PACIFIC_TIME
    today = datetime.now(team_timezone)
    midnight = today.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_midnight = midnight - timedelta(days=1)
    midnight_utc = midnight.astimezone(timezone.utc)
    yesterday_midnight_utc = yesterday_midnight.astimezone(timezone.utc)
    with Session(get_engine(team_id=team_id)) as session:
        latest_edition = session.execute(
            select(Score.edition)
            .where(
                Score.submitted_at >= yesterday_midnight_utc,
                Score.submitted_at < midnight_utc,
            )
            .order_by(desc(Score.edition))
            .limit(1)
        ).first()
        if latest_edition is None:
            return "No scores found for yesterday's Wordle! :disappointed:"
        latest_edition = latest_edition[0]
        scores = session.execute(
            select(User.slack_id, User.username, Score.edition, Score.attempts)
            .join(User.scores)
            .where(
                Score.submitted_at >= yesterday_midnight_utc,
                Score.submitted_at < midnight_utc,
                Score.edition == latest_edition,
                Score.attempts != None,
            )
            .order_by(Score.attempts)
        ).all()
    if not scores:
        return "No wins found for yesterday's Wordle! :grimacing: Hard one?"

    score_iter = iter(scores)
    current_score = next(score_iter)
    best_attempts = current_score[3]
    header = f"Wordle {latest_edition} has concluded! Congratulations to podium finishers :tada:"
    result_rows = []
    for placement in EMOJI_PLACEMENTS:
        recipients = []
        attempts = best_attempts
        while current_score is not None:
            if current_score[3] > best_attempts:
                best_attempts = current_score[3]
                break
            recipients.append(
                UserMention(slack_id=current_score[0], username=current_score[1])
            )
            current_score = next(score_iter, None)
        winners = " ".join(map(lambda recipient: recipient.encoded, recipients))
        attempts_display = f"{attempts}/{WORDLE_MAX_ATTEMPTS}" if winners else ""
        result_rows.append(f"{placement} {winners or 'None'} {attempts_display}")

    results = "\n".join(result_rows)
    return f"{header}\n\n{results}"


@daily_task(app, "shoutout_winners_posted")
def shoutout_winners(team_id: str):
    message = generate_winners_message(team_id=team_id)
    for channel_id in get_member_channel_ids(team_id=team_id):
        app.client.chat_postMessage(channel=channel_id, text=message)


def run() -> None:
    for team_id in installed_team_ids():
        shoutout_winners(team_id=team_id)


if __name__ == "__main__":
    run()
