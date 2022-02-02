import functools
from dataclasses import asdict

from ..dataclasses import (
    FROZEN_DIVIDER,
    MrkdwnBlock,
    MrkdwnSection,
    PlainTextBlock,
    PlainTextSection,
)


@functools.lru_cache()
def get_help_blocks():
    divider = asdict(FROZEN_DIVIDER)
    return [
        asdict(
            PlainTextSection(
                text=PlainTextBlock(
                    text=(
                        "Wordle stats helps you track your Wordle scores and compete with your friends and co-workers!"
                    ),
                    emoji=True,
                )
            )
        ),
        divider,
        asdict(
            MrkdwnSection(
                text=MrkdwnBlock(text="Want to submit a score?\n\n\tType `/submit`")
            )
        ),
        divider,
        asdict(
            MrkdwnSection(
                text=MrkdwnBlock(
                    text=(
                        "Want to view someone's scores?"
                        "\n\n\tType `/scores @user [@user ...]`"
                        "\n\n\tex: `/scores @TomBrady` or `/scores @Thing1 @Thing2`"
                    )
                )
            )
        ),
    ]
