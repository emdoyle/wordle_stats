import functools
from dataclasses import asdict

from app.dataclasses import MrkdwnBlock, MrkdwnSection


@functools.lru_cache()
def get_home_tab_blocks():
    return [
        asdict(
            MrkdwnSection(
                text=MrkdwnBlock(
                    text=(
                        "Wordle Stats helps you track your Wordle scores "
                        "and compete with your friends and co-workers!\n\n"
                        "Learn more by sending 'help' in a DM or mention of this app."
                    ),
                )
            )
        ),
    ]
