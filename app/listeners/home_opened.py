from sqlalchemy import select
from sqlalchemy.orm import Session

from app.apps import app
from app.blocks import get_home_tab_blocks, get_onboarding_blocks
from app.db import User, get_engine


@app.event("app_home_opened")
def handle_app_home_opened(client, body):
    event = body["event"]
    user_id = event["user"]
    channel_id = event["channel"]

    client.views_publish(
        user_id=user_id, view={"type": "home", "blocks": get_home_tab_blocks()}
    )

    view = event.get("view")
    if view is None:
        return

    team_id = view["team_id"]
    with Session(get_engine(team_id=team_id)) as session:
        user = (
            session.execute(select(User).where(User.slack_id == user_id))
            .scalars()
            .first()
        )
        if user is None:
            user = User(slack_id=user_id)
        if not user.onboarded:
            user.onboarded = True
            session.add(user)
            client.chat_postMessage(channel=channel_id, blocks=get_onboarding_blocks())
            session.commit()
