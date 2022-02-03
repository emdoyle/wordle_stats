from sqlalchemy import select
from sqlalchemy.orm import Session

from app.apps import app
from app.blocks import get_home_tab_blocks
from app.blocks.timezone import get_timezone_options
from app.constants import SELECT_TIMEZONE_ACTION_ID
from app.db import User, get_engine


@app.action(SELECT_TIMEZONE_ACTION_ID)
def handle_select_timezone(ack, client, body, action):
    ack()

    team_id = body["team"]["id"]
    user_id = body["user"]["id"]
    username = body["user"]["username"]
    timezone = action["value"]

    with Session(get_engine(team_id=team_id)) as session:
        user = (
            session.execute(select(User).where(User.slack_id == user_id))
            .scalars()
            .first()
        )
        if user is None:
            user = User(slack_id=user_id, username=username)
            session.add(user)
            session.commit()

    installation = app.installation_store.find_installation(
        enterprise_id=None, team_id=team_id
    )
    installation.set_custom_value(name="timezone", value=timezone)
    client.views_publish(
        user_id=user_id,
        view={"type": "home", "blocks": get_home_tab_blocks(timezone=timezone)},
    )


@app.options(SELECT_TIMEZONE_ACTION_ID)
def search_timezone_options(ack, options):
    ack(options=get_timezone_options(prefix=options.get("value")))
