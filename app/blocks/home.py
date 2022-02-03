import functools
from dataclasses import asdict
from typing import Optional

from app.dataclasses import FROZEN_DIVIDER, MrkdwnBlock, MrkdwnSection
from util.timezone import PACIFIC_TIMEZONE_NAME

from .timezone import get_timezone_select_section


@functools.lru_cache(maxsize=100)
def get_home_tab_blocks(timezone: Optional[str] = PACIFIC_TIMEZONE_NAME):
    divider = asdict(FROZEN_DIVIDER)
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
        divider,
        get_timezone_select_section(timezone=timezone),
    ]
