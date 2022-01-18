from . import settings
from .constants import ChannelID


def get_main_channel_id() -> str:
    if settings.DEBUG:
        return ChannelID.TESTING_MARVIN.value
    return ChannelID.WORDLE.value
