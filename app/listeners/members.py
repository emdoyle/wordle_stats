from sqlalchemy import select
from sqlalchemy.orm import Session

from app.apps import app
from app.blocks import get_onboarding_blocks
from app.db import User, get_engine


@app.event("member_joined_channel")
def handle_member_joined(client, body):
    event = body["event"]
    team_id = body["team_id"]
    user_id = event["user"]
    channel_id = event["channel"]

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
            client.chat_postEphemeral(
                user=user_id, channel=channel_id, blocks=get_onboarding_blocks()
            )
            session.commit()


@app.event("member_left_channel")
def handle_member_left():
    ...
