from sqlalchemy import select
from sqlalchemy.orm import Session

from app.apps import app
from app.blocks import get_home_tab_blocks, get_onboarding_blocks
from app.constants import TIMEZONE_CUSTOM_KEY
from app.db import User, get_engine


@app.event("app_home_opened")
def handle_app_home_opened(client, body, logger):
    logger.debug("handle_app_home_opened called")
    event = body["event"]
    if not event["tab"] == "home":
        logger.debug("Non-home tab opened event")
        return

    team_id = body["team_id"]
    user_id = event["user"]
    channel_id = event["channel"]

    installation = app.installation_store.find_installation(
        enterprise_id=None, team_id=team_id
    )
    timezone = installation.get_custom_value(name=TIMEZONE_CUSTOM_KEY)
    blocks = get_home_tab_blocks(timezone=timezone)
    logger.info("Publishing home tab for user %s in timezone %s", user_id, timezone)
    client.views_publish(user_id=user_id, view={"type": "home", "blocks": blocks})

    with Session(get_engine(team_id=team_id)) as session:
        user = (
            session.execute(select(User).where(User.slack_id == user_id))
            .scalars()
            .first()
        )
        if user is None:
            logger.info("Creating new user with slack ID %s", user_id)
            user = User(slack_id=user_id)
        if not user.onboarded:
            logger.info("Showing onboarding for user %s", user_id)
            user.onboarded = True
            session.add(user)
            client.chat_postMessage(channel=channel_id, blocks=get_onboarding_blocks())
            session.commit()
