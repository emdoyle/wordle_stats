from sqlalchemy import select
from sqlalchemy.orm import Session

from app.apps import app
from app.blocks import get_onboarding_blocks
from app.db import User, get_engine


@app.event("app_home_opened")
def handle_app_home_opened(client, body):
    user_id = body["user"]
    channel_id = body["channel"]
    view = body["view"]
    team_id = view["team_id"]
    with Session(get_engine(team_id=team_id)) as session:
        user = (
            session.execute(select(User).where(User.slack_id == user_id))
            .scalars()
            .first()
        )
        if user is not None and not user.onboarded:
            user.onboarded = True
            session.add(user)
            client.chat_postMessage(channel=channel_id, blocks=get_onboarding_blocks())
            session.commit()
