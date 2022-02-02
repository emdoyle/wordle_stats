from dataclasses import dataclass


@dataclass
class MrkdwnBlock:
    text: str
    type: str = "mrkdwn"


@dataclass
class MrkdwnSection:
    text: MrkdwnBlock
    type: str = "section"
