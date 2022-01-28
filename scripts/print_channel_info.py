from typing import Dict

from app.apps import app
from util.auth import force_client_auth
from util.teams import installed_team_ids


def display_channel(channel: Dict) -> str:
    return f"{channel['name']} ({channel['id']}): [{channel['is_member']}]"


def run() -> None:
    for team_id in installed_team_ids():
        force_client_auth(app, team_id)
        response = app.client.conversations_list(team_id=team_id)
        channels = response["channels"]
        print(
            "\n".join(
                map(
                    display_channel,
                    filter(lambda channel: channel.get("is_member", False), channels),
                )
            )
        )


if __name__ == "__main__":
    run()
