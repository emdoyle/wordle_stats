from datetime import date

from app import app
from app.channels import get_main_channel_id


def generate_wordle_thread_message() -> str:
    today = date.today()
    return f"{today.strftime('%m/%d').lstrip('0')} Solution Thread"


def run() -> None:
    app.client.chat_postMessage(
        channel=get_main_channel_id(), text=generate_wordle_thread_message()
    )


if __name__ == "__main__":
    run()
