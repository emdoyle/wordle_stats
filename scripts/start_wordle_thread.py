from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from app.apps import app
from app.constants import TIMEZONE_CUSTOM_KEY
from util.auth import force_client_auth
from util.channels import get_member_channel_ids
from util.tasks import daily_task
from util.teams import installed_team_ids
from util.timezone import PACIFIC_TIME


def generate_wordle_thread_message(timezone: Optional["ZoneInfo"] = None) -> str:
    if timezone is None:
        timezone = PACIFIC_TIME
    today = datetime.now(timezone).date()
    return f"{today.strftime('%m/%d').lstrip('0')} Solution Thread"


@daily_task(app, "solution_thread_posted")
def start_wordle_thread(team_id: str):
    installation = app.installation_store.find_installation(
        enterprise_id=None, team_id=team_id
    )
    if installation is None:
        return
    raw_timezone = installation.get_custom_value(name=TIMEZONE_CUSTOM_KEY)
    timezone = ZoneInfo(raw_timezone) if raw_timezone is not None else PACIFIC_TIME
    message = generate_wordle_thread_message(timezone=timezone)
    for channel_id in get_member_channel_ids(team_id=team_id):
        force_client_auth(app, team_id)
        app.client.chat_postMessage(channel=channel_id, text=message)


def run() -> None:
    for team_id in installed_team_ids():
        start_wordle_thread(team_id=team_id)


if __name__ == "__main__":
    run()
