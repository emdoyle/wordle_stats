from dataclasses import dataclass

SLACK_DIVIDER_TYPE = "divider"


@dataclass(frozen=True)
class Divider:
    type: str = SLACK_DIVIDER_TYPE

    def __post_init__(self):
        if self.type != SLACK_DIVIDER_TYPE:
            raise ValueError("Divider's type should not be changed.")


FROZEN_DIVIDER = Divider()
