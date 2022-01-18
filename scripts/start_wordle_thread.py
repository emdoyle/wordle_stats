from datetime import date

from app import app
from app.constants import ChannelID


def generate_wordle_thread_message() -> str:
    today = date.today()
    return f"{today.strftime('%m/%d').lstrip('0')} Solution Thread"


def run() -> None:
    app.client.chat_postMessage(
        channel=ChannelID.WORDLE.value, text=generate_wordle_thread_message()
    )


if __name__ == "__main__":
    run()
