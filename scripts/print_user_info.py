from typing import Dict

from app import app


def display_user(user: Dict) -> str:
    return f"{user['name']} / {user['profile']['display_name'] or '(n/a)'} / {user['profile']['real_name'] or '(n/a)'}"


def run() -> None:
    response = app.client.users_list()
    users = response["members"]
    print(
        "\n".join(
            map(
                display_user,
                users,
            )
        )
    )


if __name__ == "__main__":
    run()
