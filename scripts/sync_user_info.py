import logging
from dataclasses import dataclass
from typing import Dict

from slack_sdk.errors import SlackApiError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.apps import app
from app.db import User, get_engine
from util.auth import force_client_auth
from util.teams import installed_team_ids

logger = logging.getLogger()


@dataclass
class UserInfo:
    username: str = ""
    display_name: str = ""
    real_name: str = ""
    slack_id: str = ""

    @classmethod
    def from_user_data(cls, user_data: Dict) -> "UserInfo":
        return cls(
            username=user_data["name"],
            display_name=user_data["profile"]["display_name"],
            real_name=user_data["profile"]["real_name"],
            slack_id=user_data["id"],
        )


def run() -> None:
    for team_id in installed_team_ids():
        try:
            force_client_auth(app, team_id)
            response = app.client.users_list(team_id=team_id)
        except SlackApiError:
            logger.exception("Failed to sync_user_info for team %s", team_id)
            continue
        latest_user_data = response["members"]
        latest_user_data_by_username = {
            user_data["name"]: UserInfo.from_user_data(user_data)
            for user_data in latest_user_data
        }
        latest_user_data_by_slack_id = {
            user_data["id"]: UserInfo.from_user_data(user_data)
            for user_data in latest_user_data
        }
        with Session(get_engine(team_id=team_id)) as session:
            current_user_data = session.execute(select(User)).scalars().all()
            for current_user in current_user_data:
                latest_data_for_user = latest_user_data_by_username.get(
                    current_user.username
                ) or latest_user_data_by_slack_id.get(current_user.slack_id)
                if latest_data_for_user is not None:
                    print(f"Updating user: {current_user}")
                    print(f"\twith data: {latest_data_for_user}")
                    current_user.username = latest_data_for_user.username
                    current_user.display_name = latest_data_for_user.display_name
                    current_user.real_name = latest_data_for_user.real_name
                    current_user.slack_id = latest_data_for_user.slack_id
                    session.add(current_user)
            session.commit()


if __name__ == "__main__":
    run()
