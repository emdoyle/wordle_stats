from sqlalchemy import select
from sqlalchemy.orm import Session

from app.apps import app
from app.db import User, engine


def run() -> None:
    response = app.client.users_list()
    latest_user_data = response["members"]
    latest_user_data_by_username = {
        user_data["name"]: (
            user_data["profile"]["display_name"],
            user_data["profile"]["real_name"],
        )
        for user_data in latest_user_data
    }
    with Session(engine) as session:
        current_user_data = session.execute(select(User)).scalars().all()
        for current_user in current_user_data:
            latest_data_for_user = latest_user_data_by_username.get(
                current_user.username
            )
            if latest_data_for_user is not None:
                print(f"Updating user: {current_user}")
                print(f"\twith data: {latest_data_for_user}")
                current_user.display_name = latest_data_for_user[0]
                current_user.real_name = latest_data_for_user[1]
                session.add(current_user)
        session.commit()


if __name__ == "__main__":
    run()
