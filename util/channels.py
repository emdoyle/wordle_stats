from typing import List

from app import settings
from app.apps import app
from util.auth import force_client_auth


def get_member_channel_ids(team_id: str) -> List[str]:
    if settings.DEBUG:
        return [settings.TESTING_CHANNEL_ID]
    force_client_auth(app, team_id)
    response = app.client.conversations_list(team_id=team_id)
    channels = response["channels"]
    return [channel["id"] for channel in channels if channel.get("is_member", False)]
