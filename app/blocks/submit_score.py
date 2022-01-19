import functools
from dataclasses import asdict

from ..dataclasses import (
    MultiLineTextInputBlock,
    PlainTextBlock,
    PlainTextInput,
    PlainTextLabel,
    PlainTextSection,
)


@functools.lru_cache()
def get_submit_score_blocks():
    return [
        asdict(
            PlainTextSection(
                text=PlainTextBlock(
                    text="Click the 'Share' button on your Wordle screen and paste from your clipboard below!",
                    emoji=True,
                )
            )
        ),
        asdict(
            MultiLineTextInputBlock(
                label=PlainTextLabel(
                    text=":clipboard: Paste your score here:", emoji=True
                ),
                element=PlainTextInput(multiline=True, action_id="submit_score"),
            )
        ),
    ]
