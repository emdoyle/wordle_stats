from typing import Dict

from app.apps import app


def display_channel(channel: Dict) -> str:
    return f"{channel['name']} ({channel['id']}): [{channel['is_member']}]"


def run() -> None:
    response = app.client.conversations_list()
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
