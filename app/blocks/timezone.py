import functools
from dataclasses import asdict
from typing import Optional

from app.constants import SELECT_TIMEZONE_ACTION_ID
from app.dataclasses import (
    ExternalSelect,
    ExternalSelectSection,
    MrkdwnBlock,
    PlainTextBlock,
    SelectOption,
)
from util.timezone import PACIFIC_TIMEZONE_NAME, get_timezones_by_prefix


@functools.lru_cache(maxsize=100)
def get_timezone_options(prefix: str = ""):
    timezones = get_timezones_by_prefix(prefix=prefix)
    return [
        {"text": asdict(PlainTextBlock(text=timezone)), "value": timezone}
        for timezone in timezones
    ]


@functools.lru_cache(maxsize=100)
def get_timezone_select_section(timezone: Optional[str] = None):
    if timezone is None:
        timezone = PACIFIC_TIMEZONE_NAME
    return asdict(
        ExternalSelectSection(
            text=MrkdwnBlock(text="Timezone"),
            accessory=ExternalSelect(
                action_id=SELECT_TIMEZONE_ACTION_ID,
                placeholder=PlainTextBlock(text="Select your timezone"),
                initial_option=SelectOption(
                    text=PlainTextBlock(text=timezone),
                    value=timezone,
                ),
            ),
        )
    )
