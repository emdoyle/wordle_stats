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
from util.timezone import PACIFIC_TIMEZONE_NAME, display_timezone, search_timezones


def get_timezone_options(query: str = ""):
    timezones = search_timezones(query=query)
    return [
        {"text": asdict(PlainTextBlock(text=timezone_display)), "value": timezone_value}
        for timezone_display, timezone_value in timezones
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
                    text=PlainTextBlock(text=display_timezone(timezone)),
                    value=timezone,
                ),
                min_query_length=1,
            ),
        )
    )
