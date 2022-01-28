from datetime import datetime

from app.apps import app
from util.auth import force_client_auth
from util.channels import get_member_channel_ids
from util.teams import installed_team_ids
from util.timezone import PACIFIC_TIME


def generate_wordle_thread_message() -> str:
    today = datetime.now(PACIFIC_TIME).date()
    return f"{today.strftime('%m/%d').lstrip('0')} Solution Thread"


def run() -> None:
    for team_id in installed_team_ids():
        message = generate_wordle_thread_message()
        for channel_id in get_member_channel_ids(team_id=team_id):
            force_client_auth(app, team_id)
            app.client.chat_postMessage(channel=channel_id, text=message)


if __name__ == "__main__":
    run()
